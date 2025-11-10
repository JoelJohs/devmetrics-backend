from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..db import get_db
from ..security import get_current_active_user # Usas tu dependencia de usuario activo

router = APIRouter()

@router.post("/", response_model = schemas.TimeEntryRead, status_code=status.HTTP_201_CREATED)
def start_timer(entry_in: schemas.TimeEntryStart, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Inicializa un nuevo timer para el usuario
    """
    active_entry = crud.get_active_time_entry_by_user(db, user_id = current_user.id)
    if active_entry:
        raise HTTPException(status_code=400, detail="Ya existe una entrada de tiempo activa para este usuario.")

    new_entry = crud.start_time_entry(db, project_id = entry_in.project_id, user_id = current_user.id)
    if new_entry is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado o no autorizado.")
    
    return new_entry

@router.put("/stop", response_model = schemas.TimeEntryRead)
def stop_timer(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Detiene el timer activo para el usuario
    """
    active_entry = crud.get_active_time_entry_by_user(db, user_id = current_user.id)
    if not active_entry:
        raise HTTPException(status_code=400, detail="No hay una entrada de tiempo activa para este usuario.")
    
    return crud.stop_time_entry(db, db_time_entry= active_entry)

@router.get("/active", response_model = schemas.TimeEntryRead)
def get_active_timer(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Obtiene entrada de tiempo activa para el usuario
    """
    active_entry = crud.get_active_time_entry_by_user(db, user_id = current_user.id)
    if not active_entry:
        raise HTTPException(status_code=404, detail="No hay una entrada de tiempo activa para este usuario.")
    
    return active_entry

@router.get("/", response_model = List[schemas.TimeEntryRead])
def read_time_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Obtiene todas las entradas de tiempo del usuario
    """
    return crud.get_time_entries_by_user(db, user_id = current_user.id, skip=skip, limit=limit)
