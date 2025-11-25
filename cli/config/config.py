import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ---------- Declaración de constantes ----------

CONFIG_DIR = Path.home() / ".devm"
CONFIG_FILE = CONFIG_DIR / "config.json"
API_URL_BASE = os.getenv("API_URL", "http://127.0.0.1:8000/api/v1")


# ---------- Funciones de configuración ----------
def ensure_config_dir_exists():
    """
    Comprueba que exista el directorio de configuración
    """
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error: No se pudo crear el directorio de configuración en {CONFIG_DIR}", file=sys.stderr)
        sys.exit(1)

def save_token(token: str):
    """
    Guarda el token en config para las solicitudes
    """
    ensure_config_dir_exists()
    config_data = {"token": token, "api_url": API_URL_BASE}

    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)

        # Permisos de solo lectura y escritura para el usuario
        CONFIG_FILE.chmod(0o600)
        print(f"Token guardado: {CONFIG_FILE}")

    except IOError as e:
        print(f"Error: No se pudo guardar el token en {CONFIG_FILE}", file=sys.stderr)
        sys.exit(1) 

def load_token() -> str | None:
    """Carga el token guardado del archivo de configuración."""
    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (IOError, json.JSONDecodeError) as exc:
        print(f"Error leyendo la configuración: {exc}", file=sys.stderr)
        return None

    return data.get("token")