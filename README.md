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

Ejemplo con ventana y capturas:

```bash
python src/main.py --preview --save-captures --session-seconds 8 --cooldown 5 --camera 0
```

Ejemplo solo detección (sin ventana ni capturas):

```bash
python src/main.py --session-seconds 8
```

Al iniciar, el programa espera una tecla para activar la cámara. La sesión dura el tiempo configurado y luego se apaga.

## Notas

- No subas `.venv/` al repositorio.
- Si instalas nuevas librerías, actualiza `requirements.txt` manualmente o con `pip freeze > requirements.txt`.
- Las capturas se guardan en `captures/` cuando `--save-captures` está activo.
