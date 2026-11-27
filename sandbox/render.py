"""Renderings of an item and exact byte spans of the scored output.

plain (neutral, for base and instruct models):
    $ cmd1\n<terminal output 1>$ cmd2\n<terminal output 2>...$ cmdN\n<OUTPUT>$
  The scored span is OUTPUT plus the '$' of the next prompt (so the model is also charged for knowing where the
  output ends; without it a prefix like `head -n 2` vs `head -n 4` would be free).  Terminal output = stdout and
  stderr merged in arrival order, exactly as executed.  No header, no chat markup.

chat (native chat template, for instruct / post-trained models):
    user: CHAT_INSTRUCTION + "\n\n" + plain prefix (ends with "$ cmdN\n")
    assistant: OUTPUT
  The scored span is OUTPUT plus the template's end-of-turn marker (text up to the next newline after the assistant
  content, e.g. '<|im_end|>').  Both renderings normalise by len(OUTPUT)+1 bytes.
"""
PROMPT = "$ "
END = "$"
CHAT_INSTRUCTION = ("Below is a session in a Linux terminal. Reply with the exact output of the last command, "
                    "byte for byte, and nothing else.")


def prefix_of(steps):
    """steps: executed steps [{cmd, terminal}], the last one is the scored command."""
    s = "".join(PROMPT + st["cmd"] + "\n" + st["terminal"] for st in steps[:-1])
    return s + PROMPT + steps[-1]["cmd"] + "\n"


def compose(prefix, output):
    """plain text and (start, end) BYTE span of the scored output (+ terminator)."""
    text = prefix + output + END
    start = len(prefix.encode("utf-8"))
    return text, (start, start + len((output + END).encode("utf-8")))


def norm_bytes(output):
    return len(output.encode("utf-8")) + 1


def byte_to_char_span(text, span):
    b = text.encode("utf-8")
    return len(b[:span[0]].decode("utf-8")), len(b[:span[1]].decode("utf-8"))


SENT = "SCORED"


def chat_template_parts(tokenizer, prefix):
    """(pre, post_terminator) such that the chat text is pre + OUTPUT + post, and post[:k] is the end-of-turn marker."""
    msgs = [{"role": "user", "content": CHAT_INSTRUCTION + "\n\n" + prefix}, {"role": "assistant", "content": SENT}]
    kw = {}
    try:
        text = tokenizer.apply_chat_template(msgs, tokenize=False, enable_thinking=False)
    except TypeError:
        text = tokenizer.apply_chat_template(msgs, tokenize=False)
    parts = text.split(SENT)
    if len(parts) != 2:
        raise ValueError(f"chat template does not render the assistant content verbatim ({len(parts) - 1} sentinels)")
    pre, post = parts
    nl = post.find("\n")
    term = post if nl < 0 else post[:nl]
    return pre, term, post


def compose_chat(tokenizer, prefix, output, _cache={}):
    key = (id(tokenizer), prefix)
    if key not in _cache:
        _cache.clear() if len(_cache) > 4096 else None
        _cache[key] = chat_template_parts(tokenizer, prefix)
    pre, term, post = _cache[key]
    text = pre + output + post
    start = len(pre.encode("utf-8"))
    return text, (start, start + len((output + term).encode("utf-8")))
