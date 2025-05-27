from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class ProjectUserBase(BaseModel):
    username: str

class ColumnBase(BaseModel):
    name: str
    project_id: int

class ColumnCreate(ColumnBase):
    pass

class Column(ColumnBase):
    id: int
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    column_id: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    class Config:
        orm_mode = True

class TaskLog(BaseModel):
    id: int
    task_id: int
    message: str
    created_at: datetime
    class Config:
        orm_mode = True