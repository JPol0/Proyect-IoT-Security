from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import cv2


@dataclass(frozen=True)
class EvidenceResult:
    saved_path: Path | None


def ensure_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)


def build_filename(prefix: str = "person") -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{prefix}_{timestamp}.jpg"


def save_frame(frame, output_dir: Path, prefix: str = "person") -> EvidenceResult:
    ensure_output_dir(output_dir)
    filename = build_filename(prefix)
    file_path = output_dir / filename
    success = cv2.imwrite(str(file_path), frame)
    if not success:
        return EvidenceResult(saved_path=None)
    return EvidenceResult(saved_path=file_path)
