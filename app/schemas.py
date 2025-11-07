from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# -----------------------------
# Esquemas de usuario
# -----------------------------

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    username: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -----------------------------
# Esquemas de proyecto
# -----------------------------

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    owner_id: int


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None


class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# -----------------------------
# Esquemas de time entry
# -----------------------------

class TimeEntryBase(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None


class TimeEntryCreate(TimeEntryBase):
    user_id: int
    project_id: int


class TimeEntryUpdate(BaseModel):
    end_time: Optional[datetime] = None


class TimeEntryOut(TimeEntryBase):
    id: int
    user_id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True