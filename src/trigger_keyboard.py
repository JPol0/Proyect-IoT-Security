from __future__ import annotations

import time

try:
    import msvcrt
except ImportError:  # pragma: no cover - Windows-only
    msvcrt = None


def wait_for_keypress() -> str:
    if msvcrt is None:
        return input("Presiona Enter para activar la camara: ")

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            try:
                return key.decode("utf-8")
            except UnicodeDecodeError:
                return ""
        time.sleep(0.05)
