import subprocess
import sys

def run(args):
    """
    Maneja el comando link
    guarda el id del proyecto en la configuración del repositorio local
    """

    project_id = args.project_id
    print(f"Vinculando el repositorio local con el proyecto DevM ID: {project_id}")

    commands = ["git", "config", "devmetrics.projectid", str(project_id)]

    try:
        subprocess.run(commands, check=True, capture_output=True, text=True)
        print("✅ Repositorio vinculado exitosamente.")
        print(f"El repositorio local ahora está vinculado al proyecto DevM con ID: {project_id}")
        print("*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~")
        print()
        print("Puedes verificar el ID del proyecto vinculado ejecutando:")
        print("  git config devmetrics.projectid")
        print()

    except FileNotFoundError:
        print("❌ Error: El comando 'git' no se encuentra.", file=sys.stderr)
        print("Asegúrate de tener Git instalado y en tu PATH.", file=sys.stderr)
        print()
        print("Puedes descargar Git desde: https://git-scm.com/downloads", file=sys.stderr)
        print()
        sys.exit(1)
        
    except subprocess.CalledProcessError as e:
        # Esto ocurre si git devuelve un error (ej. no estás en una carpeta git)
        print("\n❌ Error: No se pudo vincular el repositorio.", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        print()
        print("¿Estás seguro de que estás dentro de un repositorio de Git iniciado?", file=sys.stderr)
        print("Intenta correr 'git init' primero si esto es un proyecto nuevo.", file=sys.stderr)
        print()
        sys.exit(1)