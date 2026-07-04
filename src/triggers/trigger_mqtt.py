from __future__ import annotations

import json
from datetime import datetime
from typing import Callable, Any
import paho.mqtt.client as mqtt

# Configuration constants for MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_ALERTA = "seguridad/alerta_movimiento"
TOPIC_CONFIRMACION = "seguridad/confirmacion_vision"


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
                timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                respuesta = {
                    "estado": "intruso_confirmado",
                    "timestamp": timestamp_actual
                }
            else:
                respuesta = {
                    "estado": "falsa_alarma"
                }
            
            json_payload = json.dumps(respuesta)
            client.publish(TOPIC_CONFIRMACION, json_payload)
            print(f"[MQTT] Veredicto JSON enviado al ESP32: {json_payload}")

    usuario_mqtt.on_connect = on_connect
    usuario_mqtt.on_message = on_message

    print("Iniciando servicio de escucha perimetral en la Laptop...")
    usuario_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
    usuario_mqtt.loop_forever()
