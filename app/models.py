from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    projects = relationship("Project", back_populates="owner")
    time_entries = relationship("TimeEntry", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    owner = relationship("User", back_populates="projects")
    time_entries = relationship("TimeEntry", back_populates="project")


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="time_entries")
    project = relationship("Project", back_populates="time_entries")

class GitEvent(Base):
    __tablename__ = "git_events"

    id = Column(Integer, primary_key=True, index=True)
    
    # Columnas de contexto de git
    branch_name = Column(String, index=True)
    commit_hash = Column(String, index=True, nullable=True)
    commit_message = Column(String, nullable=True)

    event_time = Column(DateTime, nullable=False, default = datetime.now(timezone.utc))
    
    # Relaciones
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project")

    time_entry_id = Column(Integer, ForeignKey("time_entries.id"), nullable=True)
    time_entry = relationship("TimeEntry")