import sys
import requests

from .config import API_URL_BASE

def api_login(username: str, password: str) -> str | None:
    """
    Llama a la API para loguear
    Si tiene exito, retorna el token, si no, pues nada
    """
    login_url = f"{API_URL_BASE}/auth/login/"
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(
            login_url,
            data=payload,
            timeout=10
        )
        
        if response.status_code == 401:
            print("Error: Username o contraseña incorrectos.", file=sys.stderr)
            return None
        
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            print("Error: No se recibió token de acceso.", file=sys.stderr)
            return None
        
        return access_token

    except requests.exceptions.ConnectionError:
        print(f"Error: No se pudo conectar a la API en {login_url}", file=sys.stderr)
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error de API: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error inesperado: {e}", file=sys.stderr)
        return None