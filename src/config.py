from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    preview: bool
    save_captures: bool
    session_seconds: float
    cooldown_seconds: float
    camera_index: int
    output_dir: Path
    window_name: str = "IoT Security"


def parse_args() -> AppConfig:
    parser = argparse.ArgumentParser(
        description="Local person detection with on-demand camera session",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show live window during active session",
    )
    parser.add_argument(
        "--save-captures",
        action="store_true",
        help="Save evidence images when a person is detected",
    )
    parser.add_argument(
        "--session-seconds",
        type=float,
        default=10.0,
        help="Seconds to keep the camera active per trigger",
    )
    parser.add_argument(
        "--cooldown",
        type=float,
        default=5.0,
        help="Minimum seconds between captures",
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera index (0 is usually the built-in camera)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("captures"),
        help="Directory to store evidence images",
    )
    args = parser.parse_args()

    session_seconds = max(0.0, args.session_seconds)
    cooldown_seconds = max(0.0, args.cooldown)

    return AppConfig(
        preview=args.preview,
        save_captures=args.save_captures,
        session_seconds=session_seconds,
        cooldown_seconds=cooldown_seconds,
        camera_index=args.camera,
        output_dir=args.output_dir,
    )
