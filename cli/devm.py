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
    login_parser.set_defaults(func=auth.authenticate)

    # ---------- Comando: link ----------
    # Para vincular un repositorio local con DevM
    link_parser = subparsers.add_parser("link", help="Link local repository with DevM")
    link_parser.set_defaults(func=git_utils.link_repo)

    # ---------- Comando: sync ----------
    # Para sincronizar cambios entre el repositorio local y DevM
    sync_parser = subparsers.add_parser("sync", help="Sync changes between local repo and DevM")
    sync_parser.set_defaults(func=sync.sync_changes)

    arg = parser.parse_args()
    arg.func(arg)

if __name__ == "__main__":
    main()