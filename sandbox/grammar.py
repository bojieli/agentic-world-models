"""Fixed, safe command grammar.  Every command the generator emits must pass `validate()`; the executor refuses
anything else, so no free-form shell ever reaches the sandbox.

A command line is   PART ( '; ' PART )*      with at most 2 parts, the second one only `echo $?`
a PART is           STAGE0 ( ' | ' STAGE )*  STAGE0 from HEAD_FORMS, later stages from PIPE_FORMS
Paths are relative, may contain '/' and a '*' glob, never '..', never start with '/', '~' or '-'.
"""
import re

P = r"(?!-)(?!.*\.\.)[A-Za-z0-9_*][A-Za-z0-9_.*/-]*"          # relative path (glob allowed)
N = r"[0-9]{1,3}"
WORDQ = r"'[A-Za-z0-9_:=,. -]+'"                               # quoted literal
WORD = r"[A-Za-z0-9_:=,.-]+"                                   # bare literal
LIT = rf"(?:{WORDQ}|{WORD})"
SEDX = r"'s/[A-Za-z0-9_:=,. -]+/[A-Za-z0-9_:=,. -]*/g?'"
GLOB = r"'\*?[A-Za-z0-9_.-]*\*?[A-Za-z0-9_.-]*'"
SORTF = r"(?: -n| -r| -nr| -u| -t, -k[1-9](?: -n| -nr| -r)?)?"

HEAD_FORMS = [
    rf"ls(?: -1| -1A)?(?: {P})*",
    rf"cat {P}(?: {P})*",
    rf"wc -[lwc] (?:< )?{P}",
    rf"wc -[lwc] {P}(?: {P})+",
    rf"grep(?: -[cnivlqw]{{1,3}})? {LIT}(?: {P})+",
    rf"head -n {N} {P}",
    rf"tail -n {N} {P}",
    rf"sort{SORTF} {P}",
    rf"cut -d, -f[1-9] {P}",
    rf"uniq(?: -c)? {P}",
    rf"find \.(?:/{P})?(?: -name {GLOB})?(?: -type [fd])?",
    rf"sed -n '{N}(?:,{N})?p' {P}",
    rf"sed -i {SEDX} {P}",
    rf"python {P}(?: {WORD})*",
    rf"test -[fde] {P}",
    r"echo \$\?",
    rf"echo {LIT} >> {P}",
    rf"mkdir(?: -p)? {P}",
    rf"mv {P} {P}",
    rf"cp {P} {P}",
    rf"chmod (?:000|400|444|600|644|755) {P}",
]
PIPE_FORMS = [
    rf"sort{SORTF}",
    r"uniq(?: -c)?",
    rf"head -n {N}",
    rf"tail -n {N}",
    r"wc -[lwc]",
    rf"cut -d, -f[1-9]",
    rf"grep(?: -[cniv]{{1,2}})? {LIT}",
]
_H = [re.compile(f) for f in HEAD_FORMS]
_P = [re.compile(f) for f in PIPE_FORMS]


class GrammarError(ValueError):
    pass


def validate(cmd: str) -> str:
    if any(c in cmd for c in "\n\r`$&<>(){}\\\"") and not _only_allowed_specials(cmd):
        raise GrammarError(f"forbidden character in {cmd!r}")
    parts = cmd.split("; ")
    if len(parts) > 2 or (len(parts) == 2 and parts[1] != "echo $?"):
        raise GrammarError(f"bad sequencing in {cmd!r}")
    for part in parts:
        stages = part.split(" | ")
        if not any(r.fullmatch(stages[0]) for r in _H):
            raise GrammarError(f"stage {stages[0]!r} not in grammar")
        for s in stages[1:]:
            if not any(r.fullmatch(s) for r in _P):
                raise GrammarError(f"pipe stage {s!r} not in grammar")
    return cmd


def _only_allowed_specials(cmd):
    # the only allowed uses of $ < > are 'echo $?', 'wc -x < f' and 'echo X >> f'
    c = cmd.replace("echo $?", "").replace(" >> ", " ").replace(" < ", " ")
    return not any(ch in c for ch in "\n\r`$&<>(){}\\\"")


if __name__ == "__main__":
    for ok in ["ls -1", "grep -c ERROR app.log", "cut -d, -f2 data.csv | sort | uniq -c", "test -f a.txt; echo $?",
               "echo 'buy milk' >> todo.txt", "sed -i 's/debug/release/' config.ini", "wc -l < notes.txt",
               "find . -name '*.py' -type f | sort", "python calc.py 7", "sort -t, -k2 -n people.csv | head -n 3"]:
        validate(ok)
    for bad in ["rm -rf /", "cat ../x", "cat /etc/passwd", "ls; rm a", "echo $(id)", "python -c 'import os'",
                "cat a > b", "grep x a | sh", "curl http://x"]:
        try:
            validate(bad)
        except GrammarError:
            continue
        raise SystemExit(f"accepted {bad}")
    print("grammar ok")
