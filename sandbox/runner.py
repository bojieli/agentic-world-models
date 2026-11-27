"""Runs INSIDE the sandbox container (as uid 65534, no network, read-only rootfs, tmpfs home).
stdin: one episode {"files": {path: text}, "dirs": [...], "modes": {path: octal-str}, "steps": [cmd, ...]}
stdout: {"steps": [{"cmd", "stdout", "stderr", "terminal", "rc"}], "final_tree": [...]}
Commands were validated against grammar.py on the host before being sent here.
"""
import json, os, selectors, subprocess, sys, time

os.nice(19)
ROOT = "/home/user/project"
ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/home/user", "USER": "user", "LANG": "C.UTF-8",
       "LC_ALL": "C.UTF-8", "TERM": "dumb", "PYTHONUNBUFFERED": "1", "PYTHONDONTWRITEBYTECODE": "1",
       "PYTHONHASHSEED": "0", "TZ": "UTC"}
TIMEOUT = 5


def run(cmd, last_rc):
    # '(exit N);' restores $? from the previous step, so a separate `echo $?` step behaves as in a live shell
    p = subprocess.Popen(["timeout", "-s", "KILL", str(TIMEOUT), "bash", "--norc", "--noprofile", "-c",
                          f"(exit {last_rc}); {cmd}"], cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sel = selectors.DefaultSelector()
    sel.register(p.stdout, selectors.EVENT_READ, "out")
    sel.register(p.stderr, selectors.EVENT_READ, "err")
    out, err, term = b"", b"", b""
    open_ = 2
    while open_:
        for key, _ in sel.select():
            chunk = os.read(key.fileobj.fileno(), 65536)
            if not chunk:
                sel.unregister(key.fileobj); open_ -= 1
                continue
            term += chunk                       # arrival order = what a terminal would show
            if key.data == "out":
                out += chunk
            else:
                err += chunk
    rc = p.wait()
    d = lambda b: b.decode("utf-8", "replace")
    return {"cmd": cmd, "stdout": d(out), "stderr": d(err), "terminal": d(term), "rc": rc}


def main():
    ep = json.load(sys.stdin)
    os.makedirs(ROOT)
    for d in ep.get("dirs", []):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    for path, text in ep["files"].items():
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(text)
    for path, mode in ep.get("modes", {}).items():
        os.chmod(os.path.join(ROOT, path), int(mode, 8))
    steps, rc = [], 0
    for cmd in ep["steps"]:
        r = run(cmd, rc)
        rc = r["rc"]
        steps.append(r)
    tree = []
    for dp, dn, fn in os.walk(ROOT):
        for n in fn:
            tree.append(os.path.relpath(os.path.join(dp, n), ROOT))
    json.dump({"steps": steps, "final_tree": sorted(tree)}, sys.stdout)


main()
