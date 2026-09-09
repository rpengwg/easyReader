def split_text(text, max_length=500):
    if not text:
        return []

    result = []
    buf = ""

    for char in text:
        buf += char
        if len(buf) >= max_length and char in "。！？.!?":
            result.append(buf)
            buf = ""

    if buf.strip():
        result.append(buf)

    return result
