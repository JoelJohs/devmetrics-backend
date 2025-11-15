import sys
import json
import urllib.request
import urllib.error
import urllib.parse
from cli.config import API_URL_BASE

def api_login(username: str, password: str) -> str | None:
    """
    Llama a la API para loguear
    Si tiene exito, retorna el token, si no, pues nada
    """
    login_url = f"{API_URL_BASE}/auth/signup/"
    payload = {
        "username": username,
        "password": password
    }

    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        login_url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            resp_text = response.read().decode("utf-8")
            token_data = json.loads(resp_text) if resp_text else {}
            access_token = token_data.get("access_token")
            
            if not access_token:
                print("Error: No se recibió token de acceso.", file=sys.stderr)
                return None
            
            return access_token

    except urllib.error.URLError:
        print(f"Error: No se pudo conectar a la API en {login_url}", file=sys.stderr)
        return None
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("Error: Username o contraseña incorrectos.", file=sys.stderr)
        else:
            try:
                err_text = e.read().decode("utf-8")
            except Exception:
                err_text = str(e)
            print(f"Error de API: {e.code} - {err_text}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}", file=sys.stderr)
        return None