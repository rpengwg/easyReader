import time
import pyperclip


def get_clipboard_text():
    try:
        return pyperclip.paste()
    except Exception:
        return None


def get_selected_text_by_clipboard(timeout=1):
    try:
        old = pyperclip.paste()
        pyperclip.copy("")
        time.sleep(0.1)
        text = pyperclip.paste()
        pyperclip.copy(old)
        if text and text.strip():
            return text.strip()
    except Exception:
        pass
    return None
