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
    
def post_git_event(token: str, project_id: int, branch: str, commit_hash: str, message: str):
    """
    Envía el contexto de git al backend.
    """
    url = f"{API_URL_BASE}/git-events/"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "project_id": project_id,
        "branch_name": branch,
        "commit_hash": commit_hash,
        "commit_message": message,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        print("✅ Evento de git enviado con éxito.")
        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("❌ Error: Token expirado o inválido. Por favor, ejecuta 'devm auth' de nuevo.", file=sys.stderr)
        elif e.response.status_code == 404:
            print(f"❌ Error: El proyecto ID {project_id} no existe o no tienes permiso.", file=sys.stderr)
        else:
            print(f"❌ Error de API: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Ocurrió un error al enviar datos: {e}", file=sys.stderr)
        return None