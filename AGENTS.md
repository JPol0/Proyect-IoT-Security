# AGENTS

## Quick Start
- Create and activate the virtual environment: `python -m venv .venv` then `..venv\Scripts\Activate.ps1` on PowerShell (see `README.md`).
- Install dependencies: `pip install -r requirements.txt`.
- Run the app: `python src/main.py --preview --save-captures --session-seconds 8 --cooldown 5 --camera 0`.
- YOLO mode: `python src/main.py --preview --save-captures --detector yolo --yolo-model yolov8n.pt`.

## Entry Points
- Main script: `src/main.py`.
- HOG detector: `src/detector.py`.
- YOLO detector (Ultralytics): `src/detector_yolo.py`.

## Runtime Behavior
- Program waits for a keyboard press before opening the camera.
- Session duration is controlled by `--session-seconds` and camera shuts down after it.
- Captures are saved to `captures/` only when `--save-captures` is enabled.

## Dependencies and Notes
- Core deps: `opencv-python`, `numpy`.
- YOLO requires `ultralytics` and a model file such as `yolov8n.pt`.
