from pathlib import Path


def is_odt_file(path):
    return Path(path).suffix.lower() == ".odt"


def read_odt(path):
    """Stable ODT text extraction using odfpy."""
    try:
        from odf.opendocument import load
        from odf.text import P

        doc = load(str(path))
        result = []

        for paragraph in doc.getElementsByType(P):
            text = ""
            for node in paragraph.childNodes:
                if hasattr(node, "data"):
                    text += node.data
            if text.strip():
                result.append(text.strip())

        return "\n".join(result)
    except Exception as exc:
        raise RuntimeError(f"ODT读取失败: {exc}") from exc
