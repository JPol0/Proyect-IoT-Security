from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


BoundingBox = Tuple[int, int, int, int]


@dataclass(frozen=True)
class DetectionResult:
    boxes: List[BoundingBox]
    scores: List[float]


class YoloPersonDetector:
    def __init__(self, model_path: str) -> None:
        try:
            from ultralytics import YOLO
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise ImportError(
                "Falta instalar 'ultralytics'. Ejecuta: pip install ultralytics"
            ) from exc

        self._model = YOLO(model_path)

    def detect(self, frame) -> DetectionResult:
        results = self._model.predict(frame, verbose=False)
        if not results:
            return DetectionResult(boxes=[], scores=[])

        boxes: List[BoundingBox] = []
        scores: List[float] = []

        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                if class_id != 0:
                    continue
                confidence = float(box.conf[0].item())
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                boxes.append((x1, y1, x2 - x1, y2 - y1))
                scores.append(confidence)

        return DetectionResult(boxes=boxes, scores=scores)
