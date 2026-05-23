from setuptools import setup

APP = ["copypaste.py"]

OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "CopyPaste",
        "CFBundleDisplayName": "CopyPaste",
        "CFBundleIdentifier": "com.konrad.copypaste",
        "CFBundleVersion": "0.1.0",
        "CFBundleShortVersionString": "0.1.0",
        # Background-only: no Dock icon, no menu bar entry from AppKit
        # (the menu bar icon comes from rumps instead).
        "LSUIElement": True,
    },
    "packages": ["pynput", "pyperclip", "rumps"],
    # Keep Tcl/Tk out of the bundle — we don't use tkinter, and Tk 9.0's
    # static stub archives (libtkstub.a / libtclstub.a) break py2app's
    # ad-hoc codesign step on Python 3.14.
    "excludes": ["tkinter", "test", "unittest"],
}

setup(
    app=APP,
    name="CopyPaste",
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
