from __future__ import annotations

from dataclasses import dataclass

import cv2


@dataclass(frozen=True)
class CameraConfig:
    index: int


def open_camera(config: CameraConfig) -> cv2.VideoCapture:
    capture = cv2.VideoCapture(config.index)
    return capture


def read_frame(capture: cv2.VideoCapture):
    return capture.read()


def release_camera(capture: cv2.VideoCapture) -> None:
    capture.release()
