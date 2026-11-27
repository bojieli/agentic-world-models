"""Host-side executor: runs each episode in a fresh rootless podman container.

Isolation per episode (one container each, `--rm`):
  --network=none, --read-only rootfs, tmpfs /home/user (64 MB) and /tmp (16 MB), uid/gid 65534 (nobody),
  --cap-drop=ALL, no-new-privileges, cgroup memory 512 MB + pids 128, RLIMIT_CPU 30 s, RLIMIT_FSIZE 8 MB,
  per-command `timeout -s KILL 5`, whole-container wall timeout 60 s.  The only host path visible is runner.py
  (read-only bind).  The cpu cgroup controller is not delegated to this user, so CPU share is limited by
  `nice -n 19` (podman/conmon and the runner itself) plus the worker count (<= 8) instead of --cpus.
"""
import hashlib, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

from grammar import validate

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = "docker.io/library/python:3.12-slim"
PODMAN = ["nice", "-n", "19", "podman", "run", "--rm", "-i", "--network=none", "--read-only",
          "--tmpfs", "/home/user:rw,size=64m,mode=1777,exec", "--tmpfs", "/tmp:rw,size=16m,mode=1777",
          "--user", "65534:65534", "--cap-drop=ALL", "--security-opt=no-new-privileges",
          "--memory=512m", "--memory-swap=512m", "--pids-limit=128",
          "--ulimit", "cpu=30:30", "--ulimit", "fsize=8388608:8388608", "--ulimit", "core=0:0",
          "-v", f"{HERE}/runner.py:/opt/runner.py:ro", "--workdir", "/home/user", IMAGE,
          "python", "-I", "/opt/runner.py"]


def _safe_episode(ep):
    for c in ep["steps"]:
        validate(c)
    for p in list(ep["files"]) + list(ep.get("dirs", [])) + list(ep.get("modes", {})):
        if p.startswith(("/", "~", "-")) or ".." in p.split("/"):
            raise ValueError(f"unsafe path {p}")
    return ep


def run_episode(ep):
    _safe_episode(ep)
    payload = json.dumps({k: ep[k] for k in ("files", "dirs", "modes", "steps")}).encode()
    try:
        p = subprocess.run(PODMAN, input=payload, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        return {"error": "container timeout"}
    if p.returncode != 0:
        return {"error": f"container rc={p.returncode}: {p.stderr.decode()[-500:]}"}
    return json.loads(p.stdout)


def ep_key(ep):
    return hashlib.sha1(json.dumps({k: ep[k] for k in ("files", "dirs", "modes", "steps")}, sort_keys=True).encode()).hexdigest()


def run_many(eps, workers=8, cache_path=None):
    cache = {}
    if cache_path and os.path.exists(cache_path):
        with open(cache_path) as f:
            for line in f:
                r = json.loads(line); cache[r["key"]] = r["result"]
    keys = [ep_key(e) for e in eps]
    todo = {k: e for k, e in zip(keys, eps) if k not in cache}
    print(f"[execute] {len(eps)} episodes, {len(todo)} to run, workers={workers}", file=sys.stderr, flush=True)
    out = open(cache_path, "a") if cache_path else None
    done = 0
    with ThreadPoolExecutor(workers) as ex:
        for k, r in zip(todo, ex.map(run_episode, todo.values())):
            cache[k] = r
            if out and "error" not in r:
                out.write(json.dumps({"key": k, "result": r}) + "\n")
            done += 1
            if done % 200 == 0:
                print(f"[execute] {done}/{len(todo)}", file=sys.stderr, flush=True)
    if out:
        out.close()
    return [cache[k] for k in keys]
