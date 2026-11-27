"""Select eval/calibration trajectories and observation items (measures 5/6)."""
import gzip, json, random, re, sys
from collections import defaultdict

DATA = sys.argv[1] if len(sys.argv) > 1 else "data/trajectories.jsonl.gz"
OUT = sys.argv[2] if len(sys.argv) > 2 else "prep.json"
N_EVAL, N_CAL, MAX_ITEMS, PER_TRAJ = 200, 50, 600, 3

ERR_RE = re.compile(r"Traceback \(most recent call last\)|^\s*[\w.]*(?:Error|Exception)\b:|\b(?:error|ERROR|Error)\s*:|"
                    r"command not found|No such file or directory|Permission denied|Exit code: [1-9]|"
                    r"exit (?:code|status) [1-9]|non-zero exit|\bFAILED\b|^fatal:|npm ERR!|Segmentation fault",
                    re.M)
PROMPT_RE = re.compile(r"^\S*@[\w.-]+:[^#$\n]*[#$]")  # shell prompt line (command echo)


def alloc(counts, total):
    s = sum(counts.values())
    raw = {k: total * v / s for k, v in counts.items()}
    out = {k: int(r) for k, r in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[: total - sum(out.values())]:
        out[k] += 1
    return out


def obs_reply(content):
    i = content.find("New Terminal Output:")
    body = content[i + len("New Terminal Output:"):] if i >= 0 else content
    return body.lstrip("\n").rstrip()


def new_lines(obs, prior_text):
    prior = set(l.strip() for l in prior_text.splitlines() if l.strip())
    keep = []
    for l in obs.splitlines():
        s = l.strip()
        if not s or s in prior or PROMPT_RE.match(s) or l.startswith(">"):
            continue
        keep.append(l)
    return "\n".join(keep)


def main():
    rows = [json.loads(l) for l in gzip.open(DATA, "rt")]
    held = [r for r in rows if r["split"] == "heldout"]
    by_t = defaultdict(list)
    for r in held:
        by_t[r["teacher"]].append(r)
    rng = random.Random(0)
    for t in sorted(by_t):
        rng.shuffle(by_t[t])
    counts = {t: len(v) for t, v in by_t.items()}
    a_eval, a_cal = alloc(counts, N_EVAL), alloc(counts, N_CAL)
    ev, cal = [], []
    for t in sorted(by_t):
        ev += by_t[t][: a_eval[t]]
        cal += by_t[t][a_eval[t]: a_eval[t] + a_cal[t]]
    items = []
    for r in ev:
        msgs = r["messages"]
        cand = [j for j in range(2, len(msgs)) if msgs[j]["role"] == "user"
                and msgs[j - 1]["role"] == "assistant"
                and "Are you sure you want to mark the task as complete" not in msgs[j]["content"]
                and obs_reply(msgs[j]["content"])]
        rng.shuffle(cand)
        for j in sorted(cand[:PER_TRAJ]):
            obs = obs_reply(msgs[j]["content"])
            prior = "\n".join(m["content"] for m in msgs[:j])
            stripped = new_lines(obs, prior)
            items.append(dict(traj=r["id"], msg=j, reply=obs,
                              label_raw=int(bool(ERR_RE.search(obs))),
                              label_new=int(bool(ERR_RE.search(stripped))),
                              new_text=stripped))
    rng.shuffle(items)
    items = sorted(items[:MAX_ITEMS], key=lambda x: (x["traj"], x["msg"]))
    out = dict(eval=[r["id"] for r in ev], cal=[r["id"] for r in cal], items=items,
               teachers_eval={t: a_eval[t] for t in a_eval}, teachers_cal=a_cal)
    json.dump(out, open(OUT, "w"))
    print("eval", len(ev), a_eval, "cal", len(cal), a_cal, "items", len(items),
          "pos_raw", sum(i["label_raw"] for i in items), "pos_new", sum(i["label_new"] for i in items))


if __name__ == "__main__":
    main()
