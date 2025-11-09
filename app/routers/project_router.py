from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # Usa List de typing

from .. import crud, models, schemas
from ..db import get_db
from ..security import get_current_active_user # ¡Perfecto!

router = APIRouter()

@router.post(
    "/", 
    response_model=schemas.ProjectRead, 
    status_code=status.HTTP_201_CREATED
)
def create_project_for_user(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Crea un nuevo proyecto, el cual se asigna al usuario autenticado.
    """
    return crud.create_project(db=db, project=project, owner_id=current_user.id)


@router.get("/", response_model=List[schemas.ProjectRead]) # Corregido a List
def read_projects_for_user(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Obtiene todos los proyectos del usuario autenticado.
    """
    projects = crud.get_projects_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return projects


@router.get("/{project_id}", response_model=schemas.ProjectRead)
def read_project_for_user_by_id(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Obtiene un proyecto del usuario mediante el id del proyecto.
    """
    db_project = crud.get_project_by_id(db, project_id=project_id)
    
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
        
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this project")

    return db_project


@router.put("/{project_id}", response_model=schemas.ProjectRead)
def update_project_for_user_by_id(
    project_id: int,
    project_in: schemas.ProjectUpdate, # Renombrado a project_in (buena práctica)
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Actualiza un proyecto del usuario mediante el id del proyecto.
    """
    db_project = crud.get_project_by_id(db, project_id=project_id)

    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this project")

   
    return crud.update_project(db=db, db_project=db_project, project_in=project_in)


@router.delete("/{project_id}", response_model=schemas.ProjectRead)
def delete_project_for_user_by_id(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Elimina un proyecto del usuario mediante el id del proyecto.
    """
    db_project = crud.get_project_by_id(db, project_id=project_id)

    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")


    return crud.delete_project(db=db, db_project=db_project)