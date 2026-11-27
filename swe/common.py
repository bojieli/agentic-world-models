"""Shared rendering, token classes and labels for phase-2 world-model measures (M1-M4).

All scored models share the Qwen3 tokenizer, so every tokenisation-dependent step is done once on CPU (prep2.py);
the GPU executor (run.py) only consumes token ids.
"""
import json, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


# ---------------------------------------------------------------- labeller (copied from data/build.py, which
# imports pandas/pyarrow that are optional for scoring; keep in sync with build.py)
_src = open(os.path.join(HERE, "data", "build.py")).read()
_a = _src.index("ERROR_RE = re.compile(")
_b = _src.index("# ---------------------------------------------------------------- rendering")
exec(compile(_src[_a:_b], "build.py[labeller]", "exec"))  # defines classify, label, tests_pass_from, first_programs, ...

TOKDIR = "Qwen/Qwen3-0.6B-Base"
TGRID = [round(0.7 + 0.1 * i, 2) for i in range(19)]  # 0.7 .. 2.5
NGRAM = 8
EXEC_KINDS = {"test_run", "python_exec", "shell_other"}
CONTENT_KINDS = {"file_view", "search", "edit_ack", "tool_ack"}

# ---------------------------------------------------------------- token classes (terminal classification rules + SWE)
CLS = ["ws", "boiler", "prompt", "cmd_echo", "rand_hash", "rand_time", "rand_misc", "err_line", "test_line",
       "number", "path", "other", "lineno"]
C = {c: i for i, c in enumerate(CLS)}
CONTENT_CLS = [C[c] for c in ["err_line", "test_line", "number", "path", "other", "lineno"]]
OUTCOME_CLS = [C[c] for c in ["err_line", "test_line", "number"]]
PROMPT_RE = re.compile(r"^\S*@[\w.-]+:[^#$\n]*[#$]")
BOILER_RE = re.compile(r"^(New Terminal Output:|Previous response had|WARNINGS?:|Current terminal state:|Current Terminal Screen:|Are you sure you want to mark|- Extra text detected|ERROR: (?:No valid JSON|Missing required|Invalid JSON)|Please fix these issues|\[\.\.\. output truncated \.\.\.\])")
SWE_BOILER_RE = re.compile(r"^(File updated\. Please review|Replaced \d+ occurrences?\.|Please review the changes|Your edit was not applied|Here's the result of running `cat -n`|\[scaffold error|<response clipped>|<NOTE>|=+ test session starts =+|platform \w+ -- Python|cachedir: |rootdir: |configfile: |plugins: |collecting \.\.\. |\[transformers\] |WARNING: All log messages before absl)")
ERR_RE = re.compile(r"Traceback \(most recent call last\)|^\s*[\w.]*(?:Error|Exception)\b:|\b(?:error|ERROR|Error)\s*:|command not found|No such file or directory|Permission denied|Exit code: [1-9]|exit (?:code|status) [1-9]|non-zero exit|^fatal:|npm ERR!|Segmentation fault|^\s+File \".*\", line \d+")
TEST_RE = re.compile(r"\b(?:passed|failed|PASSED|FAILED|PASS|FAIL|OK|ok|ERRORS?|collected \d+|Ran \d+ tests?|tests? (?:passed|failed)|[Ss]uccess\w*|SUCCESS)\b|✓|✗|✅|❌")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")
PATH_RE = re.compile(r"[\w.~@+-]*/[\w./~@+-]*")
HASH_RE = re.compile(r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,64}\b|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b|\b0x[0-9a-fA-F]{6,}\b|(?:[0-9a-fA-F]{2}:){3,}[0-9a-fA-F]{2}:?|(?<![\w/+=-])(?=[\w+/=-]*[A-Z])(?=[\w+/=-]*[a-z])(?=[\w+/=-]*\d)(?![\w+/=-]*(?:/app|/usr|/lib|/home|/bin|/etc|/var|/opt|site-packages))[A-Za-z0-9+/=_-]{24,}")
TIME_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?(?:[.,]\d+)?Z?)?|\b\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:\s+\d{4})?\b|\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b|\b1[67]\d{8}(?:\.\d+)?\b")
MISC_RE = re.compile(r"\btmp[\w.]{4,}|\b[Pp][Ii][Dd][ =:]*\d+|\[\d+\]\s+\d+|\b\d+(?:\.\d+)?\s?(?:ms|µs|us|ns|s|sec|secs|seconds?|min)\b|\b\d+(?:\.\d+)?\s?[kKMG]i?B/s\b|\b(?:real|user|sys)\s+\d+m[\d.]+s")
LINENO_RE = re.compile(r"^\s*(\d+)\t|^[\w./~@+-]+[:-](\d+)[:-]")
LINE_RE = re.compile(r"[^\n]*\n?")


def char_classes(text, terminal):
    """per-character class array (len(text)+1) following the terminal classification rules; `terminal` enables prompt/echo."""
    cc = np.full(len(text) + 1, C["other"], np.int8)
    boiler = BOILER_RE if terminal else SWE_BOILER_RE
    for m in LINE_RE.finditer(text):
        ln = m.group(0); s = m.start()
        if not ln:
            continue
        if boiler.match(ln):
            cc[s:m.end()] = C["boiler"]; continue
        if terminal:
            pm = PROMPT_RE.match(ln)
            if pm:
                cc[s:s + pm.end()] = C["prompt"]; cc[s + pm.end():m.end()] = C["cmd_echo"]; continue
            if ln.startswith(">"):
                cc[s:m.end()] = C["cmd_echo"]; continue
        if not ln.strip():
            continue
        base = "err_line" if ERR_RE.search(ln) else ("test_line" if TEST_RE.search(ln) else None)
        if base:
            cc[s:m.end()] = C[base]
        else:
            for rx, c in [(NUM_RE, "number"), (PATH_RE, "path")]:
                for q in rx.finditer(ln):
                    cc[s + q.start():s + q.end()] = C[c]
            lm = LINENO_RE.match(ln)
            if lm:
                g = 1 if lm.group(1) else 2
                cc[s + lm.start(g):s + lm.end(g)] = C["lineno"]
        for rx, c in [(HASH_RE, "rand_hash"), (TIME_RE, "rand_time"), (MISC_RE, "rand_misc")]:
            for q in rx.finditer(ln):
                cc[s + q.start():s + q.end()] = C[c]
    return cc


def token_classes(text, offs, terminal):
    cc = char_classes(text, terminal)
    out = np.empty(len(offs), np.int8)
    for k, (s, e) in enumerate(offs):
        piece = text[s:e]
        ls = len(piece) - len(piece.lstrip())
        out[k] = C["ws"] if ls == len(piece) else cc[s + ls]
    return out


# ---------------------------------------------------------------- tokenizer
class Enc:
    def __init__(self):
        from transformers import AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(os.environ.get("P2_TOK", TOKDIR))
        self._cache = {}

    def plain(self, s):  # wrapper text, special tokens recognised
        if s not in self._cache:
            self._cache[s] = self.tok(s, add_special_tokens=False)["input_ids"]
        return list(self._cache[s])

    def content(self, s):  # literal text with char offsets
        e = self.tok(s, add_special_tokens=False, return_offsets_mapping=True, split_special_tokens=True)
        return list(e["input_ids"]), list(e["offset_mapping"])


# ---------------------------------------------------------------- terminal echo stripping
def strip_echo(obs):
    """drop prompt+echoed-command lines and heredoc continuation lines (Terminus). Returns text."""
    keep, cont = [], False
    for l in obs.split("\n"):
        if PROMPT_RE.match(l.strip()):
            cont = True; continue
        if cont and l.startswith(">"):
            continue
        cont = False
        keep.append(l)
    return "\n".join(keep).rstrip() + ("\n" if keep else "")


def keystrokes_of(msg):
    """decode Terminus keystrokes from action parts of an assistant message"""
    out = []
    for p in msg["parts"]:
        if p[0] == "action":
            s = msg["content"][p[2]:p[3]]
            try:
                out.append(json.loads('"' + s + '"'))
            except Exception:
                out.append(s.replace("\\n", "\n"))
    return "".join(out)


ERRCLS = ["A", "B", "C", "D", "E", "F"]
ERRCLS_TEXT = ("A) ImportError or ModuleNotFoundError\nB) SyntaxError or IndentationError\n"
               "C) AssertionError or failing tests\nD) AttributeError, NameError or TypeError\n"
               "E) another Python exception (ValueError, KeyError, RuntimeError, ...)\n"
               "F) a shell or OS error (command not found, No such file or directory, Permission denied, ...)")
EXC_RE = re.compile(r"^(?:E\s+)?([A-Za-z_][\w.]*?(?:Error|Exception|Exit|Interrupt))(?::|$)", re.M)


def error_class(text):
    t = ANSI_RE.sub("", text)
    excs = [m.group(1).split(".")[-1] for m in EXC_RE.finditer(t)]
    if re.search(r"\bFAILED\b|^=+ .*\bfailed\b", t, re.M) or "AssertionError" in excs:
        return "C"
    for e in excs[::-1]:
        if e in ("ImportError", "ModuleNotFoundError"):
            return "A"
        if e in ("SyntaxError", "IndentationError", "TabError"):
            return "B"
        if e in ("AttributeError", "NameError", "TypeError"):
            return "D"
    if excs:
        return "E"
    if re.search(r"command not found|No such file or directory|Permission denied|^fatal:|cannot access", t, re.M):
        return "F"
    return "E" if "Traceback" in t else "F"
