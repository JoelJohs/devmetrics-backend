from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .security import get_password_hash
from . import models, schemas

# Operaciones CRUD para User

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