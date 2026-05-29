from __future__ import annotations

import time

import cv2

from camera import CameraConfig, open_camera, read_frame, release_camera
from config import AppConfig, parse_args
from detector import HogPersonDetector, scale_boxes
from detector_yolo import YoloPersonDetector
from evidence import save_frame
from trigger_keyboard import wait_for_keypress
from ui import close_windows, draw_boxes, draw_status, show_frame


def run_session(config: AppConfig, detector) -> None:
    camera = open_camera(CameraConfig(index=config.camera_index))
    if not camera.isOpened():
        print("No se pudo abrir la camara.")
        return

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


def main() -> None:
    config = parse_args()
    if config.detector == "yolo":
        detector = YoloPersonDetector(config.yolo_model)
    else:
        detector = HogPersonDetector()
    print("Listo. Presiona cualquier tecla para activar la camara. (q para salir)")

    while True:
        key = wait_for_keypress()
        if key.lower() == "q":
            print("Saliendo...")
            break
        run_session(config, detector)


if __name__ == "__main__":
    main()
