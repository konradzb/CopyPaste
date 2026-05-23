# CopyPaste

Tiny macOS helper for double-RDP sessions where the clipboard does not pass
through. `Cmd+C` copies normally; pressing **`Cmd+Shift+V`** types the
clipboard contents as synthetic keystrokes that the remote session sees as
ordinary typed input. `ESC` break typing.

Packaged as a standalone `.app` bundle so macOS Accessibility / Input
Monitoring permissions are granted to **CopyPaste.app only** — not to your
terminal. Lives in the menu bar (`⌘V` icon) with a Quit menu item.

## Build the .app

```sh
cd CopyPaste
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python setup.py py2app
```

Output: `dist/CopyPaste.app`. Move it to `/Applications`:

```sh
mv dist/CopyPaste.app /Applications/
```

## Run

```sh
open /Applications/CopyPaste.app
```

Or launch via Spotlight (`Cmd+Space → CopyPaste`). A `⌘V` icon appears in the
menu bar.

## macOS permissions (required on first run)

CopyPaste.app needs two permissions:

- **Accessibility** — to inject keystrokes.
- **Input Monitoring** — to listen for the global hotkey.

### Easy path (let macOS prompt you)

1. Launch `CopyPaste.app`.
2. macOS pops: *"CopyPaste wants to receive keystrokes from any application."* Click **Open System Settings**.
3. The Input Monitoring pane opens with `CopyPaste` listed. Toggle it **on** (Touch ID / password).
4. macOS asks you to **Quit & Reopen** CopyPaste — click that.
5. A second dialog appears: *"CopyPaste wants to control this computer using accessibility features."* Click **Open System Settings** and toggle `CopyPaste` **on** in the Accessibility pane.
6. Quit & Reopen one more time. The `⌘V` icon is in the menu bar — hotkey is live.

### Manual path (if you missed or dismissed the prompts)

**Grant Input Monitoring:**

1.  menu → **System Settings**.
2. Sidebar → **Privacy & Security**.
3. Scroll down → click **Input Monitoring**.
4. If `CopyPaste` is in the list, toggle it **on**. Otherwise:
   - Click the **+** button (authenticate when prompted).
   - In the file picker, navigate to `/Applications`, select **CopyPaste.app**, click **Open**.
   - Toggle it **on**.

**Grant Accessibility:**

1. Same **Privacy & Security** screen.
2. Click **Accessibility**.
3. Repeat: toggle `CopyPaste` on, or add it via **+** → `/Applications/CopyPaste.app`.

**After toggling either permission**, fully quit CopyPaste (menu bar `⌘V`
icon → **Quit CopyPaste**) and relaunch it.

## Quit

Click the `⌘V` menu bar icon → **Quit CopyPaste**.

Or from a terminal: `killall CopyPaste`.

## Keyboard layout across RDP

Mismatched keyboard layouts between macOS and the remote machine can scramble
punctuation (e.g., `.` arriving as `,`). Setting same layout on both sides e.g. **US** fixes it.

## Troubleshooting

- **Hotkey does nothing:** Input Monitoring isn't granted, or you didn't fully quit + relaunch after granting. Re-check the toggle and relaunch.
- **First character is wrong (e.g. `V` instead of `v`) or a shortcut fires:** the modifier-release step didn't catch your specific keyboard. Increase `PRE_TYPE_DELAY` in `copypaste.py` from `0.05` to `0.15`, then rebuild.
- **Permission denied / `pynput` raises on startup:** Accessibility is missing. Toggle on, quit + relaunch CopyPaste.
- **Menu bar icon never appears:** the app crashed on launch. Run from the terminal to see the traceback: `/Applications/CopyPaste.app/Contents/MacOS/CopyPaste`.
- **Rebuild fails with stale-cache errors:** delete `build/` and `dist/`, then re-run `python setup.py py2app`.
- **`codesign` fails on `libtkstub.a` / `libtclstub.a` (`RuntimeError: Cannot sign bundle`):** you're on Python 3.14. `py2app`'s ad-hoc signing can't sign Tcl/Tk 9.0's static archives. Rebuild the venv with Python **3.12** or **3.13** (`brew install python@3.12`).

