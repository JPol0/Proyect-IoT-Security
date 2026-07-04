from __future__ import annotations

import time
import cv2

from camara.camera import CameraConfig, open_camera, read_frame, release_camera
from config.config import AppConfig, parse_args
from detectors.detector import HogPersonDetector, scale_boxes
from detectors.detector_yolo import YoloPersonDetector
from config.evidence import save_frame
from ui.ui import close_windows, draw_boxes, draw_status, show_frame


def run_session(config: AppConfig, detector) -> bool:
    camera = open_camera(CameraConfig(index=config.camera_index))
    if not camera.isOpened():
        print("No se pudo abrir la camara.")
        return False

    start_time = time.time()
    last_capture_time = 0.0
    detected_once = False

    while time.time() - start_time < config.session_seconds:
        success, frame = read_frame(camera)
        if not success:
            print("No se pudo leer frame de la camara.")
            break

        resized = cv2.resize(frame, (640, 480))
        detection = detector.detect(resized)
        has_person = len(detection.boxes) > 0

        boxes = scale_boxes(detection.boxes, resized.shape, frame.shape)
        if has_person:
            detected_once = True

        if config.preview:
            draw_boxes(frame, boxes)
            draw_status(
                frame,
                "Persona detectada" if has_person else "Sin persona",
                has_person,
            )
            key = show_frame(config.window_name, frame)
            if key in (ord("q"), 27):
                break

        if config.save_captures and has_person:
            now = time.time()
            if now - last_capture_time >= config.cooldown_seconds:
                result = save_frame(frame, config.output_dir)
                if result.saved_path is not None:
                    print(f"Captura guardada: {result.saved_path}")
                else:
                    print("No se pudo guardar la captura.")
                last_capture_time = now

    release_camera(camera)
    if config.preview:
        close_windows()

    if detected_once:
        print("Sesion finalizada: se detecto persona.")
    else:
        print("Sesion finalizada: no se detecto persona.")
        
    return detected_once


def main() -> None:
    config = parse_args()
    if config.detector == "yolo":
        detector = YoloPersonDetector(config.yolo_model)
    else:
        detector = HogPersonDetector()
    
    if config.trigger == "mqtt":
        from triggers.trigger_mqtt import start_trigger
        start_trigger(config, detector, run_session)
    else:
        from triggers.trigger_keyboard import start_trigger
        start_trigger(config, detector, run_session)


if __name__ == "__main__":
    main()
