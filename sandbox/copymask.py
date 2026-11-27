"""Copy mask: which output bytes are copies of text already in the context.

An output WORD (maximal [A-Za-z0-9_]+ run) is a copy if the same whole word occurs anywhere in the context
(all commands and all earlier outputs, of BOTH variants of the pair, so one mask serves all four 2x2 terms).
mode "nocopy" (primary): purely numeric words of <= 2 digits are never masked; such tokens (counts, exit codes, line
  numbers, small computed values) occur in nearly every context by coincidence, not as copies.
mode "strict": no exemption.
mode "all": nothing masked.
Punctuation, whitespace and the end-of-output terminator are never masked (they carry line structure and the
end-of-output decision).  A model token is scored only if none of its bytes is masked.
"""
import re

WORD = re.compile(r"[A-Za-z0-9_]+")


def context_words(*contexts):
    s = set()
    for c in contexts:
        s.update(WORD.findall(c))
    return s


def copy_ranges(output, words, mode="nocopy"):
    """list of [start, end) BYTE ranges (relative to output start) that are masked."""
    if mode == "all":
        return []
    out = []
    for m in WORD.finditer(output):
        w = m.group()
        if w not in words:
            continue
        if mode == "nocopy" and w.isdigit() and len(w) <= 2:
            continue
        b0 = len(output[:m.start()].encode("utf-8"))
        out.append([b0, b0 + len(w.encode("utf-8"))])
    return out


def noncopy_words(output, words, mode="nocopy"):
    rs = {tuple(r) for r in copy_ranges(output, words, mode)}
    res = []
    for m in WORD.finditer(output):
        b0 = len(output[:m.start()].encode("utf-8"))
        if (b0, b0 + len(m.group().encode("utf-8"))) not in rs:
            res.append(m.group())
    return res


def masked_bytes(output, ranges):
    return sum(e - s for s, e in ranges)
