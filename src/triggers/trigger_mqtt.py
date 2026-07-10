from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Callable, Any
import paho.mqtt.client as mqtt

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPIC_ALERTA = "SeguridadJpol22/alertamovimiento"
TOPIC_CONFIRMACION = "SeguridadJpol22/confirmacionvision"


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
    usuario_mqtt = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[ÉXITO] Conectado al Broker MQTT de forma local.")
            client.subscribe(TOPIC_ALERTA)
        else:
            print(f"[ERROR] Conexión fallida. Código de retorno: {rc}")

    def on_message(client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        print(f"\n[MENSAJE RECIBIDO] Tópico: {msg.topic} | Payload: {payload}")
        
        if payload == "MOVIMIENTO":
            print("[PROCESO] Alerta de movimiento recibida. Activando verificación...")
            
            es_intruso = session_runner(config, detector)
            
            if es_intruso:
                estado = "intruso_confirmado"
                timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                respuesta = {
                    "estado": estado,
                    "timestamp": timestamp_actual
                }
            else:
                estado = "falsa_alarma"
                timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                respuesta = {
                    "estado": estado
                }
            
            # Registrar el evento en el JSON local
            guardar_registro_json(estado, timestamp_actual, "MQTT_trigger")
            
            json_payload = json.dumps(respuesta)
            client.publish(TOPIC_CONFIRMACION, json_payload)
            print(f"[MQTT] Veredicto JSON enviado al ESP32: {json_payload}")

    usuario_mqtt.on_connect = on_connect
    usuario_mqtt.on_message = on_message

    print("Iniciando servicio de escucha perimetral en la Laptop...")
    usuario_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
    usuario_mqtt.loop_forever()
