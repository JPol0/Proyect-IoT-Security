from __future__ import annotations

import time
import json
import os
from datetime import datetime
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


def guardar_registro_json(evento: str, timestamp: str, origen: str) -> None:
    carpeta_logs = "logs"
    archivo_log = os.path.join(carpeta_logs, "log_eventos.json")
    
    if not os.path.exists(carpeta_logs):
        os.makedirs(carpeta_logs)
        
    nuevo_registro = {
        "evento": evento,
        "timestamp": timestamp,
        "origen": origen
    }
    
    if os.path.exists(archivo_log):
        try:
            with open(archivo_log, "r", encoding="utf-8") as f:
                datos = json.load(f)
                if not isinstance(datos, list):
                    datos = []
        except (json.JSONDecodeError, IOError):
            datos = []
    else:
        datos = []
        
    datos.append(nuevo_registro)
    
    try:
        with open(archivo_log, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"[ERROR] No se pudo escribir el log de eventos: {e}")


def start_trigger(config: Any, detector: Any, session_runner: Callable[[Any, Any], bool]) -> None:
    print("Presiona una tecla para activar la camara...")
    wait_for_keypress()
    es_intruso = session_runner(config, detector)
    
    estado = "intruso_confirmado" if es_intruso else "falsa_alarma"
    timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Registrar el evento en el JSON local
    guardar_registro_json(estado, timestamp_actual, "teclado_manual")
    print(f"[LOG] Evento guardado: {estado} a las {timestamp_actual}")
