import getpass
import sys

from ..config import api, config

def authenticate(args):
    """
    Usa el comando auth para la autenticación del usuario
    Obtiene credenciales, llama a la API y guarda el token
    """

    print("=== Autenticación de Usuario en CLI de DevMetrics ===")
    username = input("Introduce tu username de DevMetrics: ")
    password = getpass.getpass("Introduce tu contraseña: ")

    access_token = api.api_login(username, password)

    if access_token:
        config.save_token(access_token)
        print("Autenticación exitosa.")
    else:
        print("Autenticación fallida.", file=sys.stderr)