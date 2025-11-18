import argparse
import sys

# import todos los paquetes
from cli.auth import auth
from cli.config import config, api
from cli.utils import git_utils, sync

def main():
    parser = argparse.ArgumentParser(description="DevM CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # ---------- Comando: auth ----------
    # Para autenticarse mediante el CLI
    login_parser = subparsers.add_parser("auth", help="Authenticate via CLI")
    login_parser.set_defaults(func=auth.run)

    # ---------- Comando: link ----------
    # Para vincular un repositorio local con DevM
    link_parser = subparsers.add_parser("link", help="Link local repository with DevM")
    link_parser.add_argument("project_id", type=int, help="ID of the DevM project to link with")
    link_parser.set_defaults(func=git_utils.run)

    # ---------- Comando: sync ----------
    # Para sincronizar cambios entre el repositorio local y DevM
    sync_parser = subparsers.add_parser("sync", help="Sync changes between local repo and DevM")
    sync_parser.set_defaults(func=sync.run)

    arg = parser.parse_args()
    arg.func(arg)

if __name__ == "__main__":
    main()