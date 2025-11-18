import getpass
import sys

from ..config import api, config

def run(args):
    """
    Usa el comando auth para la autenticación del usuario
    Obtiene credenciales, llama a la API y guarda el token
    """

    print("=== Autenticación de Usuario en CLI de DevMetrics ===")
    username = input("Introduce tu username de DevMetrics: ").strip()
    password = getpass.getpass("Introduce tu contraseña: ").strip()

    if not username:
        print("Error: El username no puede estar vacío.", file=sys.stderr)
        sys.exit(1)
    
    if not password:
        print("Error: La contraseña no puede estar vacía.", file=sys.stderr)
        sys.exit(1)

    print("🔄️ Autenticando...")

    access_token = api.api_login(username, password)

    if access_token:
        config.save_token(access_token)
        print("✅ Autenticación exitosa.")
    else:
        print("❌ Autenticación fallida.", file=sys.stderr)
        sys.exit(1)