"""Procedural generator of counterfactual tool-output items.

Each family returns  (pair_type, diff, va, vb, meta)  where va/vb are episodes
  {"files": {path: text}, "dirs": [...], "modes": {path: mode}, "steps": [cmd, ...]}
and the LAST step of each episode is the scored command.  pair_type is
  "action": same state, the commands differ (at the last step or, for `test ..` + `echo $?`, the one before);
  "state":  the final command is identical, the state differs (setup file content, or an earlier step).
Everything the model needs to predict the scored output is visible in the transcript (cat / ls / find / the edit
commands themselves); hidden setup is only ever filler.
"""
import random

WORDS = ("apple banana cherry grape lemon mango melon olive peach pear plum kiwi lime fig date guava papaya "
         "red blue green black white orange purple yellow silver gold "
         "cat dog fox owl bear wolf deer hawk frog seal crab moth "
         "river stone cloud storm field forest ocean desert island valley bridge tower garden market "
         "alpha beta gamma delta sigma omega").split()
FRUITS = WORDS[:17]
COLORS = WORDS[17:27]
ANIMALS = WORDS[27:39]
NAMES = "alice bob carol dave erin frank grace heidi ivan judy mallory nina oscar peggy quinn rupert sybil trent victor wendy".split()
DEPTS = ["eng", "ops", "sales", "hr", "legal", "design"]
CITIES = ["paris", "tokyo", "lima", "oslo", "cairo", "delhi", "quito", "rome"]
LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"]
COMPS = ["db", "api", "auth", "cache", "worker", "sched"]
MSGS = ["connection reset", "request timed out", "user login", "cache miss", "job finished", "retrying task",
        "disk usage high", "config reloaded", "token expired", "queue empty", "slow query", "health check ok"]
TASKS = ["buy milk", "call mom", "fix bug", "write report", "pay rent", "book flight", "clean desk", "read paper",
         "water plants", "update docs", "review PR", "backup laptop", "renew passport", "plan trip"]
FILLER = {"README.md": "# project\n\nSmall sandbox project.\n", "LICENSE": "MIT License\n",
          "Makefile": "all:\n\tpython main.py\n", "setup.cfg": "[metadata]\nname = demo\n",
          "requirements.txt": "requests\nnumpy\n", "main.py": "print('hello')\n", ".gitignore": "*.pyc\n__pycache__/\n",
          "CHANGELOG.md": "## 0.1.0\n- initial\n"}
DIRS = ["src", "docs", "data", "logs", "tests", "scripts", "assets", "build", "lib", "notes"]


def V(files, steps, dirs=(), modes=None):
    return {"files": dict(files), "dirs": sorted(set(dirs)), "modes": dict(modes or {}), "steps": list(steps)}


def add_filler(rng, files, k=None):
    k = rng.randint(0, 3) if k is None else k
    for n in rng.sample(sorted(FILLER), k):
        if n not in files:
            files[n] = FILLER[n]
    return files


def lines_txt(lines):
    return "".join(l + "\n" for l in lines)


def mk_log(rng, n):
    out = []
    d, h, m = rng.randint(1, 27), rng.randint(0, 20), rng.randint(0, 50)
    for _ in range(n):
        m += rng.randint(1, 9)
        if m >= 60:
            m -= 60; h += 1
        out.append(f"2024-03-{d:02d} {h:02d}:{m:02d} {rng.choice(LEVELS)} {rng.choice(COMPS)}: {rng.choice(MSGS)}")
    return out


def mk_csv_rows(rng, n):
    names = rng.sample(NAMES, n)
    return [f"{nm},{rng.choice(DEPTS)},{rng.choice(CITIES)},{rng.randint(10, 99)}" for nm in names]


def mk_nums(rng, n, lo=1, hi=200):
    return [rng.randint(lo, hi) for _ in range(n)]


def pick_distinct(rng, cands, f, k=2, tries=200):
    """k candidates whose f() values are pairwise distinct."""
    for _ in range(tries):
        c = rng.sample(cands, k)
        vals = [f(x) for x in c]
        if len(set(map(repr, vals))) == k:
            return c
    return None


# ----------------------------------------------------------------------------------------------------- S1
def s1_grep_count_pattern(rng):
    f = rng.choice(["app.log", "server.log", "events.log"])
    L = mk_log(rng, rng.randint(6, 12))
    files = add_filler(rng, {f: lines_txt(L)})
    c = pick_distinct(rng, LEVELS + COMPS, lambda p: sum(f" {p}" in l for l in L))
    if not c:
        return None
    pre = rng.choice([["ls -1", f"cat {f}"], [f"cat {f}"]])
    return ("action", "pattern", V(files, pre + [f"grep -c {c[0]} {f}"]), V(files, pre + [f"grep -c {c[1]} {f}"]), {})


def s1_grep_flag(rng):
    f = rng.choice(["notes.txt", "journal.txt", "review.txt"])
    key = rng.choice(["error", "todo", "note", "fixme"])
    L = []
    for _ in range(rng.randint(6, 11)):
        w = rng.sample(WORDS, 3)
        r = rng.random()
        kw = key if r < .25 else key.capitalize() if r < .45 else key.upper() if r < .6 else None
        if kw:
            w.insert(rng.randint(0, 3), kw)
        L.append(" ".join(w))
    files = add_filler(rng, {f: lines_txt(L)})
    flags = rng.choice([("-c", "-ci"), ("-c", "-vc"), ("-ci", "-vc"), ("-n", "-ni")])
    cmds = [f"grep {fl} {key} {f}" for fl in flags]
    return ("action", "flag", V(files, [f"cat {f}", cmds[0]]), V(files, [f"cat {f}", cmds[1]]), {})


def s1_wc_path(rng):
    a, b = rng.sample(["todo.txt", "notes.txt", "words.txt", "list.txt", "names.txt", "items.txt"], 2)
    na, nb = rng.sample(range(2, 10), 2)
    files = add_filler(rng, {a: lines_txt(rng.sample(TASKS, na)), b: lines_txt(rng.sample(WORDS, nb))})
    flag = rng.choice(["-l", "-l", "-w"])
    pre = [f"cat {a}", f"cat {b}"]
    rng.shuffle(pre)
    return ("action", "path", V(files, pre + [f"wc {flag} < {a}"]), V(files, pre + [f"wc {flag} < {b}"]), {})


def s1_wc_flag(rng):
    f = rng.choice(["todo.txt", "notes.txt", "tasks.txt"])
    files = add_filler(rng, {f: lines_txt(rng.sample(TASKS, rng.randint(3, 8)))})
    fl = rng.sample(["-l", "-w", "-c"], 2)
    return ("action", "flag", V(files, [f"cat {f}", f"wc {fl[0]} {f}"]), V(files, [f"cat {f}", f"wc {fl[1]} {f}"]), {})


def s1_count_state(rng):
    """one line of the file changed (or one extra line) -> count differs"""
    f = rng.choice(["app.log", "server.log"])
    L = mk_log(rng, rng.randint(6, 11))
    lvl = rng.choice(["ERROR", "WARN"])
    i = rng.randrange(len(L))
    L2 = list(L)
    parts = L2[i].split(" ")
    other = rng.choice([x for x in LEVELS if x != lvl])
    if parts[2] == lvl:
        parts[2] = other
    else:
        parts[2] = lvl
    L2[i] = " ".join(parts)
    mode = rng.choice(["grep", "insert"])
    if mode == "insert":
        L2 = list(L)
        L2.insert(rng.randint(0, len(L)), f"2024-03-28 23:59 {lvl} {rng.choice(COMPS)}: {rng.choice(MSGS)}")
        cmd = rng.choice([f"grep -c {lvl} {f}", f"wc -l < {f}"])
    else:
        cmd = f"grep -c {lvl} {f}"
    fa, fb = add_filler(rng, {f: lines_txt(L)}), None
    fb = dict(fa); fb[f] = lines_txt(L2)
    return ("state", "one line changed" if mode == "grep" else "one line inserted",
            V(fa, [f"cat {f}", cmd]), V(fb, [f"cat {f}", cmd]), {})


def s1_test_exists(rng):
    names = rng.sample(["notes.txt", "data.csv", "config.json", "report.md", "main.py", "todo.txt", "app.log"], 3)
    d = rng.choice(DIRS)
    files = add_filler(rng, {n: "x\n" for n in names[:2]})
    files[f"{d}/.keep"] = ""
    absent = rng.choice([names[2], names[0].split(".")[0] + rng.choice([".bak", ".old", "2.txt"])])
    kind = rng.random()
    if kind < .25:
        ta, tb = f"-d {d}", f"-d {rng.choice([x for x in DIRS if x != d])}"
    elif kind < .4:
        ta, tb = f"-f {names[0]}", f"-f {d}"
    else:
        ta, tb = f"-f {names[rng.randrange(2)]}", f"-f {absent}"
    two = rng.random() < .5
    mk = (lambda t: [f"test {t}", "echo $?"]) if two else (lambda t: [f"test {t}; echo $?"])
    pre = ["ls -1"]
    return ("action", "path", V(files, pre + mk(ta)), V(files, pre + mk(tb)), {"two_step": two})


def s1_test_state(rng):
    n = rng.choice(["notes.txt", "data.csv", "config.json", "report.md", "build"])
    files = add_filler(rng, {"main.py": "print('hi')\n"}, k=rng.randint(1, 3))
    fa = dict(files)
    if n == "build":
        fa["build/.keep"] = ""; t = "-d build"
    else:
        fa[n] = "x\n"; t = f"-f {n}"
    steps = ["ls -1", f"test {t}; echo $?"]
    return ("state", "file present vs absent", V(fa, steps), V(files, steps), {})


def s1_grep_l(rng):
    fs = rng.sample(["a.txt", "b.txt", "c.txt", "d.txt"], 3)
    fs.sort()
    files, content = {}, {}
    for f in fs:
        content[f] = rng.sample(WORDS, rng.randint(3, 5))
        files[f] = lines_txt(content[f])
    cands = sorted({w for v in content.values() for w in v})
    c = pick_distinct(rng, cands, lambda w: tuple(f for f in fs if w in content[f]))
    if not c:
        return None
    pre = [f"cat {f}" for f in fs]
    return ("action", "pattern", V(files, pre + [f"grep -l {c[0]} *.txt"]), V(files, pre + [f"grep -l {c[1]} *.txt"]), {})


def s1_ls_dir(rng):
    ds = rng.sample(DIRS, 3)
    files = {}
    for d in ds:
        for n in rng.sample(["a.py", "b.py", "index.md", "notes.txt", "data.csv", "util.py", "x.json", "run.sh"], rng.randint(1, 3)):
            files[f"{d}/{n}"] = "\n"
    add_filler(rng, files)
    a, b = rng.sample(ds, 2)
    pre = ["find . -type f | sort"]
    return ("action", "path", V(files, pre + [f"ls -1 {a}"]), V(files, pre + [f"ls -1 {b}"]), {})


def s1_grep_q_exit(rng):
    f = rng.choice(["config.ini", "settings.txt"])
    keys = rng.sample(["host", "port", "user", "mode", "debug", "timeout", "retries", "level"], 4)
    files = add_filler(rng, {f: lines_txt(f"{k}={rng.randint(1, 99)}" for k in keys[:3])})
    a, b = rng.choice(keys[:3]), keys[3]
    if rng.random() < .5:
        return ("action", "pattern", V(files, [f"cat {f}", f"grep -q {a} {f}; echo $?"]),
                V(files, [f"cat {f}", f"grep -q {b} {f}; echo $?"]), {})
    return ("action", "pattern", V(files, [f"cat {f}", f"grep {a} {f}"]), V(files, [f"cat {f}", f"grep {b} {f}"]), {})


def s1_find_name(rng):
    files = {}
    for d in rng.sample(DIRS, 3):
        for n in rng.sample(["a.py", "b.py", "index.md", "notes.txt", "data.csv", "util.py", "x.json", "guide.md"], rng.randint(2, 4)):
            files[f"{d}/{n}"] = "\n"
    exts = sorted({n.rsplit(".", 1)[1] for n in files})
    if len(exts) < 2:
        return None
    a, b = rng.sample(exts, 2)
    dirs = sorted({p.split("/")[0] for p in files})
    pre = ["ls -1"] + [f"ls -1 {d}" for d in dirs]
    return ("action", "pattern", V(files, pre + [f"find . -name '*.{a}' | sort"]),
            V(files, pre + [f"find . -name '*.{b}' | sort"]), {})


# ----------------------------------------------------------------------------------------------------- S2
LOOP_TEMPLATES = [
    "total = 0\nfor i in range({N}):\n    total += i * {K}\nprint(total)\n",
    "total = 0\nfor i in range(1, {N}):\n    total += i ** 2\nprint(total)\n",
    "a, b = 0, 1\nfor _ in range({N}):\n    a, b = b, a + b\nprint(a)\n",
    "count = 0\nfor i in range({N}):\n    if i % {K} == 0:\n        count += 1\nprint(count)\n",
    "x = 1\nfor _ in range({N}):\n    x = x * 2\nprint(x)\n",
    "s = ''\nfor i in range({N}):\n    s += str(i % {K})\nprint(s)\n",
    "nums = [i * {K} for i in range({N})]\nprint(nums)\nprint(sum(nums))\n",
    "x = {K}\nfor i in range({N}):\n    x = (x * 3 + i) % 101\nprint(x)\n",
]


def s2_loop_bound(rng):
    t = rng.choice(LOOP_TEMPLATES)
    K = rng.randint(2, 9)
    N = rng.randint(3, 12)
    N2 = N + rng.choice([-2, -1, 1, 2, 3])
    if N2 < 2:
        N2 = N + 2
    f = rng.choice(["script.py", "loop.py", "calc.py"])
    fa = add_filler(rng, {f: t.format(N=N, K=K)})
    fb = dict(fa); fb[f] = t.format(N=N2, K=K)
    steps = [f"cat {f}", f"python {f}"]
    return ("state", "loop bound", V(fa, steps), V(fb, steps), {})


ARGV_TEMPLATES = [
    "import sys\nn = int(sys.argv[1])\nresult = 1\nfor i in range(2, n + 1):\n    result *= i\nprint(result)\n",
    "import sys\nn = int(sys.argv[1])\nprint(sum(range(n + 1)))\n",
    "import sys\nn = int(sys.argv[1])\nsteps = 0\nwhile n != 1:\n    n = n // 2 if n % 2 == 0 else 3 * n + 1\n    steps += 1\nprint(steps)\n",
    "import sys\nn = int(sys.argv[1])\nprint(bin(n))\nprint(n * n)\n",
    "import sys\nn = int(sys.argv[1])\nprint('-' * n + '>')\n",
    "import sys\nn = int(sys.argv[1])\nprint([i for i in range(1, n + 1) if n % i == 0])\n",
    "import sys\nword = sys.argv[1]\nprint(word[::-1].upper(), len(word))\n",
]


def s2_argv(rng):
    i = rng.randrange(len(ARGV_TEMPLATES))
    t = ARGV_TEMPLATES[i]
    if "word" in t:
        a, b = rng.sample(WORDS, 2)
    else:
        a, b = map(str, rng.sample(range(3, 16), 2))
    f = rng.choice(["calc.py", "tool.py", "run.py"])
    files = add_filler(rng, {f: t})
    return ("action", "argument", V(files, [f"cat {f}", f"python {f} {a}"]), V(files, [f"cat {f}", f"python {f} {b}"]), {})


DATA_SCRIPTS = [
    "nums = [int(x) for x in open('{f}')]\nprint('sum:', sum(nums))\nprint('max:', max(nums))\n",
    "nums = [int(x) for x in open('{f}')]\nprint(round(sum(nums) / len(nums), 2))\n",
    "nums = [int(x) for x in open('{f}')]\nbig = [n for n in nums if n > {T}]\nprint(len(big), big)\n",
    "nums = [int(x) for x in open('{f}')]\nprint(sorted(nums)[:3])\nprint(nums.index(max(nums)))\n",
]


def s2_data_line(rng):
    f = rng.choice(["nums.txt", "values.txt", "data.txt"])
    nums = mk_nums(rng, rng.randint(4, 8), 1, 99)
    nums2 = list(nums)
    i = rng.randrange(len(nums))
    nums2[i] = rng.choice([x for x in range(1, 150) if x != nums[i]])
    s = rng.choice(DATA_SCRIPTS).format(f=f, T=rng.randint(30, 70))
    fa = add_filler(rng, {f: lines_txt(map(str, nums)), "stats.py": s})
    fb = dict(fa); fb[f] = lines_txt(map(str, nums2))
    steps = ["cat stats.py", f"cat {f}", "python stats.py"]
    return ("state", "one line changed", V(fa, steps), V(fb, steps), {})


def s2_sort_flag(rng):
    f = rng.choice(["nums.txt", "sizes.txt"]) if rng.random() < .6 else rng.choice(["words.txt", "names.txt"])
    if f in ("nums.txt", "sizes.txt"):
        items = [str(x) for x in rng.sample(list(range(1, 10)) + list(range(10, 100)) + list(range(100, 999)), rng.randint(5, 8))]
        flags = rng.choice([("", " -n"), (" -n", " -nr"), ("", " -r"), (" -r", " -nr")])
    else:
        items = rng.sample(WORDS + [w.capitalize() for w in WORDS[:10]], rng.randint(5, 8))
        flags = rng.choice([("", " -r"), ("", " -u")])
        if flags[1] == " -u":
            items += [rng.choice(items)]
            rng.shuffle(items)
    files = add_filler(rng, {f: lines_txt(items)})
    return ("action", "flag", V(files, [f"cat {f}", f"sort{flags[0]} {f}"]), V(files, [f"cat {f}", f"sort{flags[1]} {f}"]), {})


def s2_sort_key(rng):
    f = rng.choice(["people.csv", "staff.csv"])
    rows = mk_csv_rows(rng, rng.randint(5, 7))
    files = add_filler(rng, {f: lines_txt(rows)})
    opts = [" -t, -k2", " -t, -k3", " -t, -k4 -n", " -t, -k4 -nr"]
    a, b = rng.sample(opts, 2)
    tail = rng.choice(["", " | head -n 3"])
    return ("action", "flag", V(files, [f"cat {f}", f"sort{a} {f}{tail}"]), V(files, [f"cat {f}", f"sort{b} {f}{tail}"]), {})


def s2_uniq_count(rng):
    f = rng.choice(["people.csv", "staff.csv"])
    rows = mk_csv_rows(rng, rng.randint(6, 9))
    files = add_filler(rng, {f: lines_txt(rows)})
    if rng.random() < .5:
        a, b = rng.sample([2, 3], 2)
        return ("action", "flag", V(files, [f"cat {f}", f"cut -d, -f{a} {f} | sort | uniq -c"]),
                V(files, [f"cat {f}", f"cut -d, -f{b} {f} | sort | uniq -c"]), {})
    a, b = rng.sample(["sort | uniq -c", "sort | uniq", "sort -u | wc -l", "sort | uniq -c | sort -nr"], 2)
    col = rng.choice([2, 3])
    return ("action", "flag", V(files, [f"cat {f}", f"cut -d, -f{col} {f} | {a}"]),
            V(files, [f"cat {f}", f"cut -d, -f{col} {f} | {b}"]), {})


def s2_uniq_state(rng):
    f = rng.choice(["votes.txt", "colors.txt", "picks.txt"])
    pool = rng.sample(COLORS, 4)
    items = [rng.choice(pool) for _ in range(rng.randint(6, 10))]
    i = rng.randrange(len(items))
    items2 = list(items); items2[i] = rng.choice([c for c in pool if c != items[i]])
    fa = add_filler(rng, {f: lines_txt(items)})
    fb = dict(fa); fb[f] = lines_txt(items2)
    steps = [f"cat {f}", rng.choice([f"sort {f} | uniq -c", f"sort {f} | uniq -c | sort -nr", f"sort {f} | uniq | wc -l"])]
    return ("state", "one line changed", V(fa, steps), V(fb, steps), {})


STRING_TEMPLATES = [
    "word = '{w}'\nprint(word.upper())\nprint(len(word), word.count('{c}'))\n",
    "word = '{w}'\nprint(word[::-1])\nprint(sorted(set(word)))\n",
    "words = {ws}\nprint(sorted(words))\nprint(max(words, key=len))\n",
    "words = {ws}\nprint('-'.join(w[0] for w in words))\nprint(len(words))\n",
]


def s2_py_string(rng):
    t = rng.choice(STRING_TEMPLATES)
    f = rng.choice(["strings.py", "text.py"])
    if "words" in t:
        ws = rng.sample(WORDS, rng.randint(3, 5))
        ws2 = list(ws); ws2[rng.randrange(len(ws))] = rng.choice([w for w in WORDS if w not in ws])
        sa, sb = t.format(ws=ws), t.format(ws=ws2)
    else:
        w, w2 = rng.sample([x for x in WORDS if len(x) >= 4], 2)
        c = rng.choice("aeo")
        sa, sb = t.format(w=w, c=c), t.format(w=w2, c=c)
    fa = add_filler(rng, {f: sa}); fb = dict(fa); fb[f] = sb
    steps = [f"cat {f}", f"python {f}"]
    return ("state", "one line changed", V(fa, steps), V(fb, steps), {})


ARITH_TEMPLATES = [
    "a = {A}\nb = {B}\nprint(a * b + {C})\nprint(a // b, a % b)\n",
    "a = {A}\nb = {B}\nprint(a - b * {C})\nprint(max(a, b) - min(a, b))\n",
    "price = {A}\nqty = {B}\ntotal = price * qty\nprint('total:', total)\nprint('with tax:', round(total * 1.{C:02d}, 2))\n",
]


def s2_arith(rng):
    t = rng.choice(ARITH_TEMPLATES)
    A, B, C = rng.randint(10, 99), rng.randint(2, 19), rng.randint(1, 20)
    A2 = A + rng.choice([-7, -3, -1, 1, 2, 5, 11])
    f = rng.choice(["math.py", "compute.py", "bill.py"])
    which = rng.random() < .5
    sa = t.format(A=A, B=B, C=C)
    sb = t.format(A=A2, B=B, C=C) if which else t.format(A=A, B=B + rng.choice([1, 2, 3]), C=C)
    fa = add_filler(rng, {f: sa}); fb = dict(fa); fb[f] = sb
    steps = [f"cat {f}", f"python {f}"]
    return ("state", "one line changed", V(fa, steps), V(fb, steps), {})


def s2_head_tail_sort(rng):
    f = rng.choice(["scores.txt", "nums.txt"])
    nums = mk_nums(rng, rng.randint(6, 9), 1, 500)
    files = add_filler(rng, {f: lines_txt(map(str, nums))})
    k = rng.randint(1, 3)
    a, b = rng.sample([f"sort -n {f} | head -n {k}", f"sort -n {f} | tail -n {k}", f"sort -nr {f} | head -n {k}",
                       f"sort {f} | head -n {k}"], 2)
    return ("action", "flag", V(files, [f"cat {f}", a]), V(files, [f"cat {f}", b]), {})


def s2_csv_group(rng):
    rows = mk_csv_rows(rng, rng.randint(5, 8))
    i = rng.randrange(len(rows))
    r = rows[i].split(",")
    rows2 = list(rows)
    if rng.random() < .5:
        r[1] = rng.choice([d for d in DEPTS if d != r[1]])
    else:
        r[3] = str(rng.choice([x for x in range(10, 100) if str(x) != r[3]]))
    rows2[i] = ",".join(r)
    script = ("totals = {}\nfor line in open('team.csv'):\n    name, dept, city, score = line.strip().split(',')\n"
              "    totals[dept] = totals.get(dept, 0) + int(score)\nfor dept in sorted(totals):\n    print(dept, totals[dept])\n")
    fa = add_filler(rng, {"team.csv": lines_txt(rows), "group.py": script})
    fb = dict(fa); fb["team.csv"] = lines_txt(rows2)
    steps = ["cat group.py", "cat team.csv", "python group.py"]
    return ("state", "one line changed", V(fa, steps), V(fb, steps), {})


# ----------------------------------------------------------------------------------------------------- S3
def distractors(rng, others, dirs, n, allow_ls=False):
    """n commands touching only `others` (file -> list of lines) / `dirs`; never the inspected object."""
    out = []
    fs = sorted(others)
    for _ in range(n):
        f = rng.choice(fs)
        L = others[f]
        opts = [f"cat {f}", f"head -n {rng.randint(1, 3)} {f}", f"tail -n {rng.randint(1, 2)} {f}", f"wc -l < {f}",
                f"sed -n '{rng.randint(1, max(1, len(L)))}p' {f}", f"grep -c {rng.choice(L[0].split()) if L and L[0] else 'x'} {f}"]
        if dirs:
            opts.append(f"ls -1 {rng.choice(dirs)}")
        if allow_ls:
            opts.append("ls -1")
        out.append(rng.choice(opts))
    return out


def s3_env(rng, target_name, target_lines):
    others = {}
    for n in rng.sample([x for x in ["notes.txt", "words.txt", "colors.txt", "list.txt", "names.txt"] if x != target_name], 2):
        others[n] = rng.sample(WORDS if n != "names.txt" else NAMES, rng.randint(2, 4))
    d = rng.choice(DIRS)
    files = {target_name: lines_txt(target_lines)}
    for n, L in others.items():
        files[n] = lines_txt(L)
    files[f"{d}/readme.txt"] = "docs\n"
    return files, others, [d]


def _s3_assemble(rng, files_a, files_b, intro, change_a, change_b, others, dirs, final, allow_ls=False, pre_n=None):
    pre_n = rng.randint(0, 2) if pre_n is None else pre_n
    gap = rng.randint(2, 6)                             # inspection happens `gap` steps after the change
    pre = distractors(rng, others, dirs, pre_n, allow_ls)
    mid = distractors(rng, others, dirs, gap - 1, allow_ls)
    ca = change_a if isinstance(change_a, list) else [change_a]
    cb = change_b if isinstance(change_b, list) else [change_b]
    sa = intro + pre + ca + mid + [final]
    sb = intro + pre + cb + mid + [final]
    return V(files_a, sa, dirs), V(files_b, sb, dirs), {"gap": gap, "change_step": len(intro) + len(pre)}


def s3_append_present(rng):
    t = rng.choice(["todo.txt", "tasks.txt", "shopping.txt"])
    L = rng.sample(TASKS, rng.randint(2, 5))
    new = rng.choice([x for x in TASKS if x not in L])
    files, others, dirs = s3_env(rng, t, L)
    o = rng.choice(sorted(others))
    final = rng.choice([f"wc -l < {t}", f"wc -w < {t}", f"grep -c '{new.split()[0]}' {t}", f"sort {t} | uniq | wc -l"])
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}"], f"echo '{new}' >> {t}", f"echo '{new}' >> {o}",
                             others, dirs, final)
    return ("state", "edit target (present vs absent on inspected file)", va, vb, m)


def s3_sed_present(rng):
    t = rng.choice(["config.ini", "settings.conf"])
    keys = rng.sample(["mode", "host", "port", "level", "user", "cache", "workers"], 4)
    vals = {"mode": ["debug", "release"], "host": ["localhost", "example.org"], "port": ["8080", "9090"],
            "level": ["info", "warn"], "user": ["admin", "guest"], "cache": ["on", "off"], "workers": ["4", "16"]}
    L = [f"{k}={vals[k][0]}" for k in keys]
    k = rng.choice(keys)
    files, others, dirs = s3_env(rng, t, L)
    o = rng.choice(sorted(others))
    old, new = vals[k]
    final = rng.choice([f"grep -c {new} {t}", f"grep -c {old} {t}", f"grep -c {k}={old} {t}"])
    change_a = f"sed -i 's/{k}={old}/{k}={new}/' {t}"
    change_b = rng.choice([f"sed -i 's/{k}={old}/{k}={new}/' {o}", f"cat {o}"])
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}"], change_a, change_b, others, dirs, final)
    return ("state", "edit present vs absent", va, vb, m)


def s3_mv_cp(rng):
    t = rng.choice(["report.txt", "draft.md", "data.csv", "photo.jpg"])
    files, others, dirs = s3_env(rng, t, ["content"])
    arch = rng.choice(["archive", "backup", "old"])
    files[f"{arch}/.keep"] = ""
    dirs = dirs + [arch]
    final = rng.choice(["ls -1 | wc -l", f"test -f {t}; echo $?", f"ls -1 {arch} | wc -l", "find . -type f | wc -l"])
    if final == f"ls -1 {arch} | wc -l":
        ca, cb = f"mv {t} {arch}/", rng.choice([f"cp {others and sorted(others)[0]} {arch}/", f"cat {t}"])
    else:
        ca, cb = f"mv {t} {arch}/", f"cp {t} {arch}/"
    va, vb, m = _s3_assemble(rng, files, files, ["ls -1"], ca, cb, others, [d for d in dirs if d != arch], final)
    return ("state", "mv vs cp", va, vb, m)


def s3_append_value(rng):
    t = rng.choice(["nums.txt", "values.txt"])
    nums = mk_nums(rng, rng.randint(3, 6), 10, 90)
    files, others, dirs = s3_env(rng, t, map(str, nums))
    files["total.py"] = f"nums = [int(x) for x in open('{t}')]\nprint(len(nums), sum(nums))\n"
    v1, v2 = rng.sample([3, 7, 42, 99, 150, 500, 1], 2)
    final = rng.choice([f"sort -n {t} | tail -n 1", "python total.py", "python total.py", f"sort -n {t} | head -n 1"])
    intro = [f"cat {t}"] + (["cat total.py"] if final == "python total.py" else [])
    va, vb, m = _s3_assemble(rng, files, files, intro, f"echo {v1} >> {t}", f"echo {v2} >> {t}", others, dirs, final)
    return ("state", "different appended value", va, vb, m)


def s3_cp_alias(rng):
    t = rng.choice(["config.ini", "notes.txt", "list.txt"])
    w = rng.sample(COLORS, 3)
    L = [f"color={x}" for x in w]
    files, others, dirs = s3_env(rng, t, L)
    b = t.replace(".", "_copy.")
    old = w[rng.randrange(3)]
    new = rng.choice([c for c in COLORS if c not in w])
    final = rng.choice([f"grep -c {new} {t}", f"grep -c {old} {t}", f"grep -c {new} {t} {b}"])
    intro = [f"cat {t}", f"cp {t} {b}"]
    va, vb, m = _s3_assemble(rng, files, files, intro, f"sed -i 's/{old}/{new}/' {b}", f"sed -i 's/{old}/{new}/' {t}",
                             others, dirs, final)
    return ("state", "edit copy vs original", va, vb, m)


def s3_multi_append(rng):
    t = rng.choice(["log.txt", "journal.txt"])
    L = rng.sample(WORDS, rng.randint(2, 4))
    files, others, dirs = s3_env(rng, t, L)
    o = rng.choice(sorted(others))
    k = rng.randint(2, 4)
    adds = [f"echo {w} >> {t}" for w in rng.sample(WORDS, k)]
    j = rng.randrange(k)
    alt = adds[j].replace(f">> {t}", f">> {o}")
    final = rng.choice([f"wc -l < {t}", f"wc -c < {t}"])
    # changes are interleaved with distractors; the counterfactual step is adds[j]
    seq_a, seq_b = [], []
    for i, ad in enumerate(adds):
        seq_a.append(ad); seq_b.append(alt if i == j else ad)
        if i < k - 1 and rng.random() < .5:
            d = distractors(rng, others, dirs, 1)[0]
            seq_a.append(d); seq_b.append(d)
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}"], seq_a, seq_b, others, dirs, final, pre_n=0)
    return ("state", "one of several appends present vs absent", va, vb, m)


def s3_mkdir_mv_find(rng):
    files, others, dirs = s3_env(rng, "main.py", ["print('hi')"])
    files["util.py"] = "x = 1\n"
    newd = rng.choice(["pkg", "app", "core"])
    mover = rng.choice(["util.py", "main.py"])
    ca = [f"mkdir {newd}", f"mv {mover} {newd}/"]
    cb = [f"mkdir {newd}", f"cp {mover} {newd}/"] if rng.random() < .5 else [f"mkdir {newd}", f"cat {mover}"]
    final = rng.choice(["find . -name '*.py' | wc -l", "ls -1 | wc -l", f"test -f {mover}; echo $?", f"ls -1 {newd} | wc -l"])
    va, vb, m = _s3_assemble(rng, files, files, ["ls -1"], ca, cb, others, dirs, final)
    return ("state", "mv present vs absent", va, vb, m)


def s3_sed_count(rng):
    t = rng.choice(["app.log", "server.log"])
    L = mk_log(rng, rng.randint(5, 9))
    files, others, dirs = s3_env(rng, t, L)
    a, b = rng.sample(["WARN", "ERROR", "INFO", "DEBUG"], 2)
    o = rng.choice(sorted(others))
    final = rng.choice([f"grep -c {b} {t}", f"grep -c {a} {t}"])
    ca = f"sed -i 's/{a}/{b}/g' {t}"
    cb = rng.choice([f"sed -i 's/{a}/{b}/g' {o}", f"sed -i 's/{b}/{a}/g' {t}"])
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}"], ca, cb, others, dirs, final)
    return ("state", "different edit", va, vb, m)


def s3_sed_number_python(rng):
    t = "config.ini"
    keys = rng.sample(["rate", "qty", "workers", "days", "hours", "price"], 3)
    vals = {k: rng.randint(2, 12) for k in keys}
    files, others, dirs = s3_env(rng, t, [f"{k}={v}" for k, v in vals.items()])
    op = rng.choice(["*", "+", "-"])
    files["calc.py"] = ("cfg = {}\nfor line in open('config.ini'):\n    k, v = line.strip().split('=')\n    cfg[k] = int(v)\n"
                        f"print(cfg['{keys[0]}'] {op} cfg['{keys[1]}'])\nprint(sum(cfg.values()))\n")
    k = rng.choice(keys)
    new = rng.choice([x for x in range(2, 20) if x != vals[k]])
    ca = f"sed -i 's/{k}={vals[k]}/{k}={new}/' {t}"
    o = rng.choice(sorted(others))
    cb = rng.choice([f"cat {o}", f"sed -i 's/{k}={vals[k]}/{k}={new}/' {o}",
                     f"sed -i 's/{k}={vals[k]}/{k}={rng.choice([x for x in range(2, 20) if x not in (new, vals[k])])}/' {t}"])
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}", "cat calc.py"], ca, cb, others, dirs, "python calc.py")
    return ("state", "config edit present vs absent / different value", va, vb, m)


def s3_append_python(rng):
    t = rng.choice(["nums.txt", "scores.txt"])
    nums = mk_nums(rng, rng.randint(2, 4), 2, 40)
    files, others, dirs = s3_env(rng, t, map(str, nums))
    files["stats.py"] = rng.choice([
        f"nums = [int(x) for x in open('{t}')]\nprint('n =', len(nums))\nprint('sum =', sum(nums))\n",
        f"nums = [int(x) for x in open('{t}')]\nprint(max(nums) - min(nums))\nprint(sum(nums) // len(nums))\n"])
    o = rng.choice(sorted(others))
    k = rng.randint(2, 3)
    vals = [rng.randint(1, 60) for _ in range(k)]
    adds = [f"echo {v} >> {t}" for v in vals]
    j = rng.randrange(k)
    alt = rng.choice([adds[j].replace(f">> {t}", f">> {o}"), f"echo {vals[j] + rng.randint(1, 9)} >> {t}"])
    seq_a, seq_b = [], []
    for i, ad in enumerate(adds):
        seq_a.append(ad); seq_b.append(alt if i == j else ad)
        if i < k - 1 and rng.random() < .6:
            d = distractors(rng, others, dirs, 1)[0]
            seq_a.append(d); seq_b.append(d)
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}", "cat stats.py"], seq_a, seq_b, others, dirs,
                             "python stats.py", pre_n=0)
    return ("state", "one of several appends absent / different value", va, vb, m)


# ----------------------------------------------------------------------------------------------------- S4
def s4_py_index(rng):
    f = rng.choice(["items.py", "pick.py", "show.py"])
    items = rng.sample(FRUITS, rng.randint(3, 5))
    n = len(items)
    good, bad = rng.randrange(n), rng.choice([n, n + 1, n + 3, -(n + 1)])
    t = "items = {items}\nprint('count:', len(items))\nprint(items[{i}])\n"
    fa = add_filler(rng, {f: t.format(items=items, i=good)}); fb = dict(fa); fb[f] = t.format(items=items, i=bad)
    steps = [f"cat {f}", f"python {f}"]
    return ("state", "index in range vs out of range", V(fa, steps), V(fb, steps), {"err": "IndexError"})


def s4_py_where(rng):
    f = rng.choice(["check.py", "lookup.py"])
    a = rng.sample(FRUITS, 3); b = rng.sample(ANIMALS, 4)
    t = "a = {a}\nb = {b}\nprint('first:', a[{i}])\nprint('second:', b[{j}])\nprint('done')\n"
    sa = t.format(a=a, b=b, i=3 + rng.randint(0, 2), j=rng.randrange(4))
    sb = t.format(a=a, b=b, i=rng.randrange(3), j=4 + rng.randint(0, 2))
    fa = add_filler(rng, {f: sa}); fb = dict(fa); fb[f] = sb
    steps = [f"cat {f}", f"python {f}"]
    return ("state", "error location", V(fa, steps), V(fb, steps), {"err": "IndexError@line"})


SYNTAX_BASE = ["def total(xs):", "    s = 0", "    for x in xs:", "        s += x", "    return s", "",
               "print(total([1, 2, 3]))"]


def s4_py_syntax(rng):
    f = rng.choice(["total.py", "sum.py"])
    bugs = {"colon_def": (0, "def total(xs)"), "colon_for": (2, "    for x in xs"),
            "paren": (6, "print(total([1, 2, 3])"), "indent": (3, "    s += x"), "bracket": (6, "print(total([1, 2, 3)))"),
            "keyword": (4, "    retrun s")}
    a, b = rng.sample(sorted(bugs) + ["none"], 2)
    def src(k):
        L = list(SYNTAX_BASE)
        if k != "none":
            i, line = bugs[k]; L[i] = line
        return lines_txt(L)
    fa = add_filler(rng, {f: src(a)}); fb = dict(fa); fb[f] = src(b)
    steps = [f"cat {f}", f"python {f}"]
    return ("state", f"syntax bug {a} vs {b}", V(fa, steps), V(fb, steps), {"err": "SyntaxError"})


def s4_py_exc_type(rng):
    f = rng.choice(["nums.txt", "input.txt"])
    nums = [str(x) for x in mk_nums(rng, rng.randint(3, 5), 1, 9)]
    i = rng.randrange(len(nums))
    va_, vb_ = rng.sample(["0", "abc", "x1", "", "2.5", str(rng.randint(1, 9))], 2)
    na, nb = list(nums), list(nums)
    na[i], nb[i] = va_, vb_
    script = f"for line in open('{f}'):\n    n = int(line)\n    print(100 // n)\n"
    fa = add_filler(rng, {f: lines_txt(na), "divide.py": script}); fb = dict(fa); fb[f] = lines_txt(nb)
    steps = ["cat divide.py", f"cat {f}", "python divide.py"]
    return ("state", "data line changed (exception type)", V(fa, steps), V(fb, steps), {"err": "ValueError/ZeroDivisionError"})


def s4_py_keyerror(rng):
    keys = rng.sample(["name", "version", "port", "debug", "owner", "region"], 3)
    vals = {"name": '"demo"', "version": '"1.2.0"', "port": "8080", "debug": "true", "owner": '"ops"', "region": '"eu"'}
    want = keys[rng.randrange(3)]
    alt = rng.choice([k for k in ["name", "version", "port", "debug", "owner", "region"] if k not in keys])
    def js(ks):
        return "{\n" + ",\n".join(f'  "{k}": {vals[k]}' for k in ks) + "\n}\n"
    keys_b = [alt if k == want else k for k in keys]
    script = f"import json\ncfg = json.load(open('config.json'))\nprint('keys:', len(cfg))\nprint(cfg['{want}'])\n"
    fa = add_filler(rng, {"config.json": js(keys), "show.py": script}); fb = dict(fa); fb["config.json"] = js(keys_b)
    steps = ["cat config.json", "cat show.py", "python show.py"]
    return ("state", "key present vs renamed", V(fa, steps), V(fb, steps), {"err": "KeyError"})


def s4_py_nameerror(rng):
    f = rng.choice(["report.py", "count.py"])
    L = ["total = 0", "for n in [4, 8, 15]:", "    total += n", "print('total', total)", "average = total / 3",
         "print('average', average)"]
    typos = {2: "    total += m", 3: "print('total', totl)", 4: "average = totals / 3", 5: "print('average', avg)"}
    a, b = rng.sample(["none", 2, 3, 4, 5], 2)
    def src(k):
        X = list(L)
        if k != "none":
            X[k] = typos[k]
        return lines_txt(X)
    fa = add_filler(rng, {f: src(a)}); fb = dict(fa); fb[f] = src(b)
    steps = [f"cat {f}", f"python {f}"]
    return ("state", f"typo at line {a} vs {b}", V(fa, steps), V(fb, steps), {"err": "NameError"})


def s4_json_decode(rng):
    keys = rng.sample(["name", "version", "port", "debug", "owner"], 3)
    vals = {"name": '"demo"', "version": '"1.2.0"', "port": "8080", "debug": "true", "owner": '"ops"'}
    good = [f'  "{k}": {vals[k]}' for k in keys]
    def render(lines, trailing=False):
        body = ",\n".join(lines) + ("," if trailing else "")
        return "{\n" + body + "\n}\n"
    bad_kinds = ["trailing", "quote", "colon", "none"]
    a, b = rng.sample(bad_kinds, 2)
    def mk(kind):
        L = list(good)
        if kind == "trailing":
            return render(L, True)
        j = rng.randrange(3)
        if kind == "quote":
            L[j] = L[j].replace(f'"{keys[j]}"', f"'{keys[j]}'")
        elif kind == "colon":
            L[j] = L[j].replace(":", "")
        return render(L)
    script = "import json\ncfg = json.load(open('config.json'))\nfor k, v in cfg.items():\n    print(k, '=', v)\n"
    fa = add_filler(rng, {"config.json": mk(a), "load.py": script}); fb = dict(fa); fb["config.json"] = mk(b)
    steps = ["cat load.py", "cat config.json", "python load.py"]
    return ("state", f"json {a} vs {b}", V(fa, steps), V(fb, steps), {"err": "JSONDecodeError"})


def s4_missing_file(rng):
    names = rng.sample(["notes.txt", "todo.txt", "data.csv", "app.log", "readme.txt"], 2)
    files = add_filler(rng, {names[0]: lines_txt(rng.sample(WORDS, rng.randint(2, 4)))})
    d = rng.choice(DIRS); files[f"{d}/x.txt"] = "x\n"
    tool = rng.choice(["cat {}", "head -n 2 {}", "wc -l {}", "grep -c a {}", "sort {}"])
    miss = rng.choice([names[1], names[0].replace(".", "s."), d])
    return ("action", "path", V(files, ["ls -1", tool.format(names[0])]), V(files, ["ls -1", tool.format(miss)]),
            {"err": "No such file / Is a directory"})


def s4_py_missing_file(rng):
    data = rng.choice(["data.csv", "input.txt", "scores.txt"])
    rows = [str(x) for x in mk_nums(rng, rng.randint(3, 5), 1, 50)]
    script = f"with open('{data}') as f:\n    nums = [int(x) for x in f]\nprint(sum(nums))\n"
    files = add_filler(rng, {data: lines_txt(rows), "sum.py": script})
    old = data.replace(".", "_old.")
    ca, cb = f"mv {data} {old}", f"cp {data} {old}"
    steps = lambda c: [f"cat {data}", "cat sum.py", c, "ls -1", "python sum.py"]
    return ("state", "mv vs cp before run", V(files, steps(ca)), V(files, steps(cb)), {"err": "FileNotFoundError"})


def s4_permission(rng):
    f = rng.choice(["secret.txt", "keys.txt", "private.log"])
    files = add_filler(rng, {f: lines_txt(rng.sample(WORDS, 2))})
    form = rng.random()
    if form < .5:
        a, b = rng.sample(["000", "644", "400", "600"], 2) if rng.random() < .3 else ("000", rng.choice(["644", "444"]))
        final = rng.choice([f"cat {f}", f"head -n 1 {f}", f"wc -l {f}"])
    else:
        a, b = "444", "644"
        files["write.py"] = f"with open('{f}', 'a') as fh:\n    fh.write('new\\n')\nprint(open('{f}').read())\n"
        final = "python write.py"
    pre = ["ls -1"] + (["cat write.py"] if final == "python write.py" else [])
    return ("state", f"chmod {a} vs {b}", V(files, pre + [f"chmod {a} {f}", final]), V(files, pre + [f"chmod {b} {f}", final]),
            {"err": "Permission denied"})


def s4_mkdir_exists(rng):
    d = rng.choice(DIRS)
    files = add_filler(rng, {"main.py": "print(1)\n"}, k=rng.randint(1, 3))
    fa = dict(files); fa[f"{d}/.keep"] = ""
    final = rng.choice([f"mkdir {d}", f"mkdir {d}; echo $?", f"mkdir {d}/sub; echo $?"])
    return ("state", "dir exists vs not", V(fa, ["ls -1", final]), V(files, ["ls -1", final]), {"err": "File exists"})


def s4_exit_code(rng):
    f = rng.choice(["notes.txt", "list.txt"])
    files = add_filler(rng, {f: lines_txt(rng.sample(WORDS, 3))})
    miss = rng.choice(["missing.txt", f.replace(".txt", ".md"), "notes2.txt"])
    w = rng.choice(files[f].split())
    form = rng.choice(["ls", "grep", "grepw"])
    if form == "ls":
        a, b = f"ls {f}; echo $?", f"ls {miss}; echo $?"
    elif form == "grep":
        a, b = f"grep -q {w} {miss}; echo $?", f"grep -q {w} {f}; echo $?"
    else:
        a, b = f"grep {w} {f}; echo $?", f"grep {w} {miss}; echo $?"
    return ("action", "path/pattern", V(files, ["ls -1", f"cat {f}", a]), V(files, ["ls -1", f"cat {f}", b]),
            {"err": "exit code 1/2"})


# ----------------------------------------------------------------------------------------------------- S2h (hard)
# Computed values whose dependence on the changed input is NON-MONOTONE (modular arithmetic, digit sums, bit ops,
# nested-loop counts), so "bigger input -> bigger number" style heuristics cannot bind; the change is minimal (+-1..3).

def h_mod_loop(rng):
    f = rng.choice(["mix.py", "rng.py", "step.py"])
    S, A, M = rng.randint(1, 9), rng.randint(3, 13), rng.choice([97, 101, 89, 53])
    N = rng.randint(3, 9)
    t = "x = {S}\nfor i in range({N}):\n    x = (x * {A} + i) % {M}\nprint(x)\nprint(x % 10)\n"
    if rng.random() < .5:
        sa, sb, d = t.format(S=S, N=N, A=A, M=M), t.format(S=S, N=N + 1, A=A, M=M), "loop bound +1"
    else:
        sa, sb, d = t.format(S=S, N=N, A=A, M=M), t.format(S=S, N=N, A=A + rng.choice([1, 2]), M=M), "multiplier changed"
    fa = add_filler(rng, {f: sa}); fb = dict(fa); fb[f] = sb
    steps = [f"cat {f}", f"python {f}"]
    return ("state", d, V(fa, steps), V(fb, steps), {})


def h_mod_arith(rng):
    f = rng.choice(["calc.py", "mod.py"])
    a, b = rng.randint(12, 99), rng.randint(3, 40)
    M1, M2 = rng.choice([7, 9, 11, 13, 17]), rng.choice([19, 23, 29, 31])
    t = "a = {a}\nb = {b}\nprint((a * b) % {M1})\nprint((a + 3 * b) % {M2})\nprint(a * b // {M2})\n"
    if rng.random() < .5:
        sb = t.format(a=a + rng.choice([-2, -1, 1, 2, 3]), b=b, M1=M1, M2=M2)
    else:
        sb = t.format(a=a, b=b + rng.choice([-1, 1, 2]), M1=M1, M2=M2)
    fa = add_filler(rng, {f: t.format(a=a, b=b, M1=M1, M2=M2)}); fb = dict(fa); fb[f] = sb
    steps = [f"cat {f}", f"python {f}"]
    return ("state", "one literal changed", V(fa, steps), V(fb, steps), {})


ARGV_HARD = [
    "import sys\nn = int(sys.argv[1])\nsq = n * n\nprint(sq % 100)\nprint(sum(int(d) for d in str(sq)))\n",
    "import sys\nn = int(sys.argv[1])\nwhile n >= 10:\n    n = sum(int(d) for d in str(n))\nprint(n)\n",
    "import sys\nn = int(sys.argv[1])\nprint(n ^ {K}, n & {K})\nprint(bin(n).count('1'))\n",
    "import sys\nn = int(sys.argv[1])\nsteps = 0\nwhile n != 1:\n    n = n // 2 if n % 2 == 0 else 3 * n + 1\n    steps += 1\nprint(steps)\n",
    "import sys\nn = int(sys.argv[1])\nprint(sum(i for i in range(n) if i % 3 == 1 or i % 5 == 2) % 50)\n",
    "import sys\nw = sys.argv[1]\nprint(sum(ord(c) for c in w) % 100)\nprint(len(set(w)), w.count('a') + w.count('e'))\n",
]


def h_argv(rng):
    i = rng.randrange(len(ARGV_HARD))
    t = ARGV_HARD[i].replace("{K}", str(rng.choice([5, 6, 9, 10, 12])))
    if "w = " in t:
        a, b = rng.sample([w for w in WORDS if len(w) >= 4], 2)
    elif i == 1:
        a = rng.randint(100, 9999); b = a + rng.choice([1, 2, 3]); a, b = str(a), str(b)
    else:
        a = rng.randint(5, 40); b = a + rng.choice([1, 2, 3]); a, b = str(a), str(b)
    f = rng.choice(["calc.py", "tool.py", "num.py"])
    files = add_filler(rng, {f: t})
    return ("action", "argument", V(files, [f"cat {f}", f"python {f} {a}"]), V(files, [f"cat {f}", f"python {f} {b}"]), {})


def h_nested(rng):
    f = rng.choice(["pairs.py", "count.py"])
    N, K = rng.randint(4, 9), rng.randint(3, 7)
    t = "count = 0\nfor i in range({N}):\n    for j in range(i):\n        if (i + j) % {K} == 0:\n            count += 1\nprint(count)\n"
    sb = t.format(N=N + 1, K=K) if rng.random() < .5 else t.format(N=N, K=K + 1)
    fa = add_filler(rng, {f: t.format(N=N, K=K)}); fb = dict(fa); fb[f] = sb
    steps = [f"cat {f}", f"python {f}"]
    return ("state", "bound or modulus changed", V(fa, steps), V(fb, steps), {})


def h_list_key(rng):
    f = rng.choice(["nums.txt", "data.txt"])
    nums = mk_nums(rng, rng.randint(5, 7), 10, 99)
    nums2 = list(nums); j = rng.randrange(len(nums)); nums2[j] = nums[j] + rng.choice([-2, -1, 1, 2, 3])
    script = rng.choice([
        f"nums = [int(x) for x in open('{f}')]\nprint(sum(x for x in nums if x % 3 == 0))\nprint(sum(x % 10 for x in nums))\n",
        f"nums = [int(x) for x in open('{f}')]\nprint(sorted(nums, key=lambda x: (x % 10, x))[0])\nprint(sum(nums) % 13)\n",
        f"nums = [int(x) for x in open('{f}')]\nodd = [x for x in nums if x % 2]\nprint(len(odd), sum(odd) % 100)\n"])
    fa = add_filler(rng, {f: lines_txt(map(str, nums)), "agg.py": script}); fb = dict(fa); fb[f] = lines_txt(map(str, nums2))
    steps = ["cat agg.py", f"cat {f}", "python agg.py"]
    return ("state", "one value +-small", V(fa, steps), V(fb, steps), {})


def h_csv_filter(rng):
    rows = mk_csv_rows(rng, rng.randint(6, 8))
    T = rng.randint(35, 70)
    city = rng.choice(CITIES)
    script = ("import sys\nt = int(sys.argv[1])\nn = s = 0\nfor line in open('team.csv'):\n    name, dept, city, score = line.strip().split(',')\n"
              "    if int(score) > t:\n        n += 1\n        s += int(score) % 10\nprint(n, s)\n")
    files = add_filler(rng, {"team.csv": lines_txt(rows), "filt.py": script})
    scores = sorted(int(r.split(",")[3]) for r in rows)
    T2 = T + rng.choice([-9, -6, -3, 3, 6, 9])
    return ("action", "threshold argument", V(files, ["cat filt.py", "cat team.csv", f"python filt.py {T}"]),
            V(files, ["cat filt.py", "cat team.csv", f"python filt.py {T2}"]), {})


# ----------------------------------------------------------------------------------------------------- S3h (hard)
# Several edits (to the inspected file AND to other files) interleaved with distractors; exactly one of them differs
# between the variants; the inspection is a count or a non-monotone computation over the tracked state.

def _interleave(rng, edits_a, edits_b, others, dirs):
    sa, sb = [], []
    for ea, eb in zip(edits_a, edits_b):
        sa.append(ea); sb.append(eb)
        for d in distractors(rng, others, dirs, rng.randint(0, 2)):
            sa.append(d); sb.append(d)
    return sa, sb


def h3_grep_net(rng):
    t = rng.choice(["app.log", "events.log"])
    L = mk_log(rng, rng.randint(4, 7))
    files, others, dirs = s3_env(rng, t, L)
    o = rng.choice(sorted(others))
    P = rng.choice(["ERROR", "WARN"])
    Q = rng.choice([x for x in ["INFO", "DEBUG"]])
    pool = [f"echo '2024-03-29 10:00 {P} api: retry' >> {t}", f"sed -i 's/{Q}/{P}/' {t}", f"sed -i 's/{P}/{Q}/' {t}",
            f"echo '2024-03-29 11:00 {Q} db: ok' >> {t}", f"sed -i 's/{Q}/{P}/g' {t}"]
    k = rng.randint(3, 5)
    edits = [rng.choice(pool) for _ in range(k)]
    j = rng.randrange(k)
    alt = list(edits)
    alt[j] = rng.choice([edits[j].replace(f" {t}", f" {o}"), rng.choice([p for p in pool if p != edits[j]])])
    sa, sb = _interleave(rng, edits, alt, others, dirs)
    final = rng.choice([f"grep -c {P} {t}", f"grep -c {Q} {t}", f"wc -l < {t}"])
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}"], sa, sb, others, dirs, final, pre_n=0)
    return ("state", "one of several mixed edits differs", va, vb, dict(m, n_edits=k))


def h3_mv_chain(rng):
    files, others, dirs = s3_env(rng, "notes.txt", ["x"])
    names = rng.sample(["a.txt", "b.txt", "c.txt", "d.txt", "e.txt"], 4)
    for n in names:
        files[n] = "x\n"
    A, B = rng.sample(["inbox", "done", "archive", "keep"], 2)
    steps = [f"mkdir {A}", f"mkdir {B}"]
    ops = []
    for n in rng.sample(names, 3):
        d = rng.choice([A, B])
        ops.append(f"{rng.choice(['mv', 'mv', 'cp'])} {n} {d}/")
    ops.append(f"mv {A}/{ops[0].split()[1]} {B}/" if ops[0].startswith("mv") and f"{A}/" in ops[0] else f"cp {names[-1]} {A}/")
    j = rng.randrange(len(ops) - 1)
    alt = list(ops)
    cmd, src, dst = ops[j].split()
    alt[j] = f"{'cp' if cmd == 'mv' else 'mv'} {src} {dst}" if rng.random() < .5 else f"{cmd} {src} {B if dst == A + '/' else A}/"
    sa, sb = _interleave(rng, steps + ops, steps + alt, others, [])
    final = rng.choice(["ls -1 | wc -l", f"ls -1 {A} | wc -l", f"ls -1 {B} | wc -l", "find . -name '*.txt' | wc -l",
                        f"find . -name '{src}' | wc -l"])
    va, vb, m = _s3_assemble(rng, files, files, ["ls -1"], sa, sb, others, [], final, pre_n=0)
    return ("state", "one mv/cp differs (op or destination)", va, vb, m)


def h3_config_mod(rng):
    t = "config.ini"
    keys = rng.sample(["rate", "qty", "workers", "days", "hours", "price"], 3)
    vals = {k: rng.randint(2, 15) for k in keys}
    files, others, dirs = s3_env(rng, t, [f"{k}={v}" for k, v in vals.items()])
    M = rng.choice([7, 11, 13])
    files["calc.py"] = ("cfg = {}\nfor line in open('config.ini'):\n    k, v = line.strip().split('=')\n    cfg[k] = int(v)\n"
                        f"print((cfg['{keys[0]}'] * cfg['{keys[1]}'] + cfg['{keys[2]}']) % {M})\n")
    cur = dict(vals)
    edits, alts = [], []
    for _ in range(rng.randint(2, 3)):
        k = rng.choice(keys); new = rng.choice([x for x in range(2, 20) if x != cur[k]])
        edits.append(f"sed -i 's/{k}={cur[k]}/{k}={new}/' {t}"); cur[k] = new
    j = rng.randrange(len(edits))
    alts = list(edits)
    alts[j] = edits[j].replace(f" {t}", f" {rng.choice(sorted(others))}")
    sa, sb = _interleave(rng, edits, alts, others, dirs)
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}", "cat calc.py"], sa, sb, others, dirs, "python calc.py", pre_n=0)
    return ("state", "one of several config edits absent", va, vb, m)


def h3_append_mod(rng):
    t = rng.choice(["nums.txt", "scores.txt"])
    nums = mk_nums(rng, rng.randint(2, 4), 2, 40)
    files, others, dirs = s3_env(rng, t, map(str, nums))
    M = rng.choice([7, 9, 11])
    files["stats.py"] = f"nums = [int(x) for x in open('{t}')]\nprint(len(nums), sum(nums) % {M})\n"
    vals = [rng.randint(1, 60) for _ in range(rng.randint(3, 4))]
    adds = [f"echo {v} >> {t}" for v in vals]
    j = rng.randrange(len(adds))
    alt = list(adds)
    alt[j] = rng.choice([adds[j].replace(f">> {t}", f">> {rng.choice(sorted(others))}"), f"echo {vals[j] + rng.randint(1, 6)} >> {t}"])
    sa, sb = _interleave(rng, adds, alt, others, dirs)
    va, vb, m = _s3_assemble(rng, files, files, [f"cat {t}", "cat stats.py"], sa, sb, others, dirs, "python stats.py", pre_n=0)
    return ("state", "one of several appends absent / different value", va, vb, m)


FAMILIES = {
    "S1": [s1_grep_count_pattern, s1_grep_flag, s1_wc_path, s1_wc_flag, s1_count_state, s1_test_exists, s1_test_state,
           s1_grep_l, s1_ls_dir, s1_grep_q_exit, s1_find_name],
    "S2": [s2_loop_bound, s2_argv, s2_data_line, s2_sort_flag, s2_sort_key, s2_uniq_count, s2_uniq_state, s2_py_string,
           s2_arith, s2_head_tail_sort, s2_csv_group],
    "S3": [s3_append_present, s3_sed_present, s3_mv_cp, s3_append_value, s3_cp_alias, s3_multi_append,
           s3_mkdir_mv_find, s3_sed_count, s3_sed_number_python, s3_append_python],
    "S4": [s4_py_index, s4_py_where, s4_py_syntax, s4_py_exc_type, s4_py_keyerror, s4_py_nameerror, s4_json_decode,
           s4_missing_file, s4_py_missing_file, s4_permission, s4_mkdir_exists, s4_exit_code],
    "S2h": [h_mod_loop, h_mod_arith, h_argv, h_nested, h_list_key, h_csv_filter],
    "S3h": [h3_grep_net, h3_mv_chain, h3_config_mod, h3_append_mod],
}


def candidates(stratum, n, seed):
    """n candidate specs for a stratum, round-robin over families, each from its own seeded RNG."""
    fams = FAMILIES[stratum]
    out, i, tries = [], 0, 0
    while len(out) < n and tries < n * 5:
        fam = fams[tries % len(fams)]
        rng = random.Random(f"{seed}/{stratum}/{tries}")
        tries += 1
        r = fam(rng)
        if r is None:
            continue
        pair_type, diff, va, vb, meta = r
        swap = rng.random() < .5                         # orientation of (a, a') is random -> null has mean 0
        if swap:
            va, vb = vb, va
        out.append({"id": f"{stratum}-{len(out):04d}", "stratum": stratum, "family": fam.__name__, "pair_type": pair_type,
                    "diff": diff, "meta": dict(meta, swapped=swap), "variants": [va, vb], "gen_seed": f"{seed}/{stratum}/{tries - 1}"})
    return out
