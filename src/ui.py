from __future__ import annotations

from typing import List, Tuple

import cv2

BoundingBox = Tuple[int, int, int, int]


def draw_boxes(frame, boxes: List[BoundingBox]) -> None:
    for x, y, w, h in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)


def draw_status(frame, message: str, detected: bool) -> None:
    color = (0, 200, 0) if detected else (0, 0, 200)
    cv2.putText(
        frame,
        message,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2,
        cv2.LINE_AA,
    )


def show_frame(window_name: str, frame) -> int:
    cv2.imshow(window_name, frame)
    return cv2.waitKey(1) & 0xFF


def close_windows() -> None:
    cv2.destroyAllWindows()
