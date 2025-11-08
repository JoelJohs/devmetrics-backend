from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Imports de funnciones internar y necesarias
from .. import crud, models, schemas, security
from ..db import get_db

router = APIRouter()

# Endpoint para registrar un nuevo usuario en la aplicacion
@router.post("/singup", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Se recibe un JSON con email, password y los campos opcionales.
    """
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if user.username:
        db_user_username = crud.get_user_by_username(db, username=user.username)
        if db_user_username:
            raise HTTPException(status_code=400, detail="Username already registered")
        
    # Si el correo y el username no existen se crea el usuario
    new_user = crud.create_user(db=db, user=user)
    return new_user

# Endpoint para login de usuario y obtencion de token JWT
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Se recibe un formulario con username y password para autenticacion.
    """
    user = crud.get_user_by_username(db, username=form_data.username)

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}