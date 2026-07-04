from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import cv2

BoundingBox = Tuple[int, int, int, int]


@dataclass(frozen=True)
class DetectionResult:
    boxes: List[BoundingBox]
    weights: List[float]


class HogPersonDetector:
    def __init__(self) -> None:
        self._hog = cv2.HOGDescriptor()
        self._hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, frame) -> DetectionResult:
        boxes, weights = self._hog.detectMultiScale(
            frame,
            winStride=(8, 8),
            padding=(8, 8),
            scale=1.05,
        )
        return DetectionResult(boxes=list(boxes), weights=[float(w) for w in weights])


def scale_boxes(boxes: List[BoundingBox], source_shape, target_shape) -> List[BoundingBox]:
    source_h, source_w = source_shape[:2]
    target_h, target_w = target_shape[:2]
    scale_x = target_w / float(source_w)
    scale_y = target_h / float(source_h)

    scaled: List[BoundingBox] = []
    for x, y, w, h in boxes:
        scaled.append(
            (
                int(x * scale_x),
                int(y * scale_y),
                int(w * scale_x),
                int(h * scale_y),
            )
        )
    return scaled
