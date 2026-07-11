# Proyecto IoT Security

## Requisitos

- Python 3.10 o superior

## Instalación

1. Crear el entorno virtual:

```bash
python -m venv .venv
```

2. Activar el entorno virtual en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si usas CMD:

```cmd
.venv\Scripts\activate.bat
```

Si usas Bash:

```bash
source .venv/Scripts/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

El archivo principal es `src/main.py`. Ejecuta desde el entorno virtual activado.

El programa admite configurar el desencadenador (trigger) que activa la cámara mediante la opción `--trigger`:
- `keyboard` (por defecto): Espera una pulsación de tecla local para iniciar la sesión.
- `mqtt`: Escucha alertas en el broker MQTT (`seguridad/alerta_movimiento` con payload `MOVIMIENTO`) para iniciar la sesión y publica los resultados en `seguridad/confirmacion_vision`.

Ejemplo con trigger de teclado (por defecto), ventana y capturas:

```bash
python src/main.py --trigger keyboard --preview --save-captures --session-seconds 8 --cooldown 5 --camera 0
```

Ejemplo con trigger MQTT y detector YOLO:

```bash
python src/main.py --trigger mqtt --preview --save-captures --detector yolo --yolo-model yolov8n.pt
```

Ejemplo solo detección (sin ventana ni capturas):

```bash
python src/main.py --session-seconds 8
```

## Notas

- No subas `.venv/` al repositorio.
- Si instalas nuevas librerías, actualiza `requirements.txt` manualmente o con `pip freeze > requirements.txt`.
- Las capturas se guardan en `captures/` cuando `--save-captures` está activo.
- Los registros se guardan en `logs/` cuando `--save-logs` está activo.

## Configuración del Hardware

El sistema incluye una capa física con un ESP32 que requiere la siguiente asignación de pines (GPIO):
- **LED Verde:** GPIO 12
- **LED Rojo:** GPIO 14
- **LED Amarillo:** GPIO 27
- **Simulador PIR:** GPIO 13

**Librerías necesarias en Arduino IDE:**
Para compilar y cargar el código en el ESP32, es obligatorio instalar:
- `PubSubClient` (para la conexión MQTT).
- Soporte para la tarjeta **ESP32** (por Espressif Systems) desde el Gestor de Tarjetas.
