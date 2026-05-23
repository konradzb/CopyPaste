import threading
import time

import pyperclip
import rumps
from pynput import keyboard
from pynput.keyboard import Controller, Key

HOTKEY = "<cmd>+<shift>+v"
PER_CHAR_DELAY = 0.008
PRE_TYPE_DELAY = 0.05

controller = Controller()


def release_modifiers():
    # Cmd+Shift+V is still physically held when the callback fires; without
    # releasing them the first synthesized keystrokes would be interpreted
    # as modified shortcuts on the remote side.
    for mod in (Key.cmd, Key.cmd_l, Key.cmd_r, Key.shift, Key.shift_l, Key.shift_r):
        try:
            controller.release(mod)
        except Exception:
            pass


def quick_type():
    text = pyperclip.paste()
    if not text:
        return
    release_modifiers()
    time.sleep(PRE_TYPE_DELAY)
    for ch in text:
        controller.type(ch)
        time.sleep(PER_CHAR_DELAY)


def run_listener():
    with keyboard.GlobalHotKeys({HOTKEY: quick_type}) as h:
        h.join()


def main():
    threading.Thread(target=run_listener, daemon=True).start()
    rumps.App("CopyPaste", title="⌘V").run()


if __name__ == "__main__":
    main()
