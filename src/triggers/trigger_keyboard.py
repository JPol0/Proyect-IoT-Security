from __future__ import annotations

import time
from typing import Callable, Any

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


def start_trigger(config: Any, detector: Any, session_runner: Callable[[Any, Any], bool]) -> None:
    print("Presiona una tecla para activar la camara...")
    wait_for_keypress()
    session_runner(config, detector)

