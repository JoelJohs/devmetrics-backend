import sys
from ..config import config, api
from . import git_utils

def run(args):
    """
    Maneja el comando 'sync'.
    Sincroniza los cambios entre el repositorio local y DevM
    """
    print("⏳ Sincronizando cambios...")
    
    token = config.load_token()
    if not token:
        print("❌ Error: No se encontró un token de autenticación. Por favor, ejecuta 'devm auth' para iniciar sesión.", file=sys.stderr)
        sys.exit(1)
        
    # Ahora sí funcionará porque agregamos la función en git_utils
    project_id = git_utils.get_linked_project_id()
    if not project_id:
        print("❌ Error: El repositorio no está vinculado a ningún proyecto DevM. Por favor, ejecuta 'devm link <project_id>' para vincularlo.", file=sys.stderr)
        sys.exit(1)

    try:
        project_id = int(project_id)
    except ValueError:
        print("❌ Error: El ID del proyecto en la configuración local no es válido.", file=sys.stderr)
        sys.exit(1)

    print("🔍 Buscando contexto de git...") # (Corregido typo 'maginifying glass')
    try:
        branch = git_utils.get_current_branch()
        commit_hash = git_utils.get_latest_commit_hash()
        commit_message = git_utils.get_latest_commit_message()

        print(f"📋 Contexto detectado:")
        print(f"   - Proyecto ID: {project_id}")
        print(f"   - Rama: {branch}")
        print(f"   - Commit: {commit_hash[:7]}")

    except Exception as e:
        print(f"❌ Error al obtener el contexto de git: {e}", file=sys.stderr)
        sys.exit(1)

    print("🚀 Enviando datos al backend de DevM...")
    result = api.post_git_event(token, project_id, branch, commit_hash, commit_message)

    if result:
        print("✅ Sincronización completada con éxito.")

        # CORRECCIÓN AQUÍ: Usar 'time_entry_id' (como en el schema del backend)
        timer_id = result.get("time_entry_id") 
        
        if timer_id:
            print(f"🔗 Contexto enlazado a la sesión de trabajo activa (Timer ID: {timer_id})")
        else:
            print("ℹ️  Evento guardado. (No se detectó un timer activo en este momento).")

    else:
        print("❌ La sincronización falló.", file=sys.stderr)
        sys.exit(1)