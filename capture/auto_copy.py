import time
from pynput.keyboard import Controller, Key

from config import COPY_WAIT
from capture.clipboard import get_text, set_text

keyboard = Controller()


def copy_selection():
    """Copy the current selection without leaving the user's copied text changed."""
    previous = get_text()
    try:
        keyboard.press(Key.ctrl)
        keyboard.press("c")
        keyboard.release("c")
        keyboard.release(Key.ctrl)
        time.sleep(COPY_WAIT)
        text = get_text()
        return text.strip() if text else None
    finally:
        # Clipboard restoration is intentionally delayed slightly so the target
        # application has completed its copy operation.
        if previous is not None:
            time.sleep(0.03)
            set_text(previous)
