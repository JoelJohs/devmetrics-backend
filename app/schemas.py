from pydantic import BaseModel, ConfigDict, EmailStr
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

    model_config = ConfigDict(from_attributes=True)


# -----------------------------
# Esquemas de proyecto
# -----------------------------

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------------------
# Esquemas de time entry
# -----------------------------
class TimeEntryStart(BaseModel):
    project_id: int

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

    model_config = ConfigDict(from_attributes=True)

class TimeEntryRead(BaseModel):
    id: int
    project_id: int
    user_id: int
    description: str | None = None
    start_time: datetime
    end_time: datetime | None = None
    duration: int | None = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# -----------------------------
# Esquemas de eventos git
# -----------------------------
class GitEventCreate(BaseModel):
    project_id: int
    branch_name: str
    commit_hash: Optional[str] = None
    commit_message: Optional[str] = None

class GitEventRead(BaseModel):
    id: int
    branch_name: str
    commit_hash: Optional[str] = None
    commit_message: Optional[str] = None
    event_time: datetime
    # Las relaciones
    owner_id: int
    project_id: int
    time_entry_id: Optional[int] = None 

    model_config = ConfigDict(from_attributes=True)

# -----------------------------
# Esquemas de autenticacion
# -----------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None