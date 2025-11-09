from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .security import get_password_hash
from . import models, schemas

# -----------------------------
# Operaciones CRUD para User
# -----------------------------

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Crea un nuevo usuario en la base de datos a partir del esquema UserCreate.
    """
    # Hasehea la contraseña antes de almacenarla por seguridad
    hashed_password = get_password_hash(user.password)

    # Crea el objeto de usuario de la base de datos basado en el esquema
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,

        # Campos de auditoría para seguimiento de creación y actualización
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    # Guardado de sesion de la base de datos
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Busca a un usuario mediante su correo electrónico.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> models.User | None:
    """
    Busca a un usuario mediante su nombre de usuario.
    """
    return db.query(models.User).filter(models.User.username == username).first()

# -----------------------------
# Operaciones CRUD para Project
# -----------------------------

def get_project_by_id(db: Session, project_id: int):
    """
    Busca un proyecto por su ID.
    """
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los proyectos del usuario especifico
    """
    return db.query(models.Project).filter(models.Project.owner_id == owner_id).order_by(models.Project.created_at.desc()).offset(skip).limit(limit).all()

def create_project(db: Session, project: schemas.ProjectCreate, owner_id: int):
    """
    Crea un nuevo proyecto
    """
    db_project = models.Project(
        **project.model_dump(),
        owner_id=owner_id, # Asigna el propietario
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

def update_project(db: Session, db_project: models.Project, project_in: schemas.ProjectUpdate):
    """
    Actualiza un proyecto existente
    """
    update_data = project_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_project, key, value)

    db_project.updated_at = datetime.now(timezone.utc)

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

def delete_project(db: Session, db_project: models.Project):
    """
    Elimina un proyecto existente
    """
    db.delete(db_project)
    db.commit()

    return db_project

# -----------------------------