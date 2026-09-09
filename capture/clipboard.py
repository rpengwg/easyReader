import ctypes
import time

CF_UNICODETEXT = 13
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def _get_text():
    if not user32.OpenClipboard(None):
        return None
    try:
        if not user32.IsClipboardFormatAvailable(CF_UNICODETEXT):
            return None
        handle = user32.GetClipboardData(CF_UNICODETEXT)
        if not handle:
            return None
        pointer = kernel32.GlobalLock(handle)
        if not pointer:
            return None
        try:
            return ctypes.wstring_at(pointer)
        finally:
            kernel32.GlobalUnlock(handle)
    finally:
        user32.CloseClipboard()


def get_text(retries=8, delay=0.03):
    for _ in range(retries):
        text = _get_text()
        if text is not None:
            return text
        time.sleep(delay)
    return None


def set_text(text, retries=8, delay=0.03):
    if text is None:
        return False
    for _ in range(retries):
        if user32.OpenClipboard(None):
            try:
                user32.EmptyClipboard()
                data = ctypes.create_unicode_buffer(text)
                size = ctypes.sizeof(data)
                handle = kernel32.GlobalAlloc(0x0002, size)
                pointer = kernel32.GlobalLock(handle)
                ctypes.memmove(pointer, ctypes.addressof(data), size)
                kernel32.GlobalUnlock(handle)
                if user32.SetClipboardData(CF_UNICODETEXT, handle):
                    return True
                kernel32.GlobalFree(handle)
            finally:
                user32.CloseClipboard()
        time.sleep(delay)
    return False
