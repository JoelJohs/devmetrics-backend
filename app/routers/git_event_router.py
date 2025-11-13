from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..db import get_db
from ..security import get_current_active_user

router = APIRouter()

@router.post("/", response_model=schemas.GitEventRead, status_code=status.HTTP_201_CREATED)
def create_git_context_event(
    event_in: schemas.GitEventCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Crea un nuevo evento git.
    """
    db_event = crud.create_git_event(db = db, event_in = event_in, owner_id = current_user.id)

    if db_event is None:
        raise HTTPException(status_code=404, detail="Project not found or you do not have permission.")
    
    return db_event

@router.get("/", response_model=List[schemas.GitEventRead])
def read_git_events(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    """
    Obtiene todos los eventos git del usuario.
    """
    db_events = crud.get_git_events_by_user(db = db, owner_id = current_user.id)
    return db_events
    