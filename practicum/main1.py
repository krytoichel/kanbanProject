from typing import Optional, Annotated

from fastapi import FastAPI, APIRouter
from fastapi.params import Depends
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()

class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None
    columns_id: Optional[int] = 0

class STask(STaskAdd):
    id: int

class SProjectAdd(BaseModel):
    name: str
    projects_id: Optional[int] = 0

class SProject(SProjectAdd):
    id: int

class SColumnsAdd(BaseModel):
    name: str
    columns_id: Optional[int] = 0

class SColumn(SColumnsAdd):
    id: int

tasks = []
projects = []
columns = []

@router.post("/projects/{project_id}", tags=["Projects"])
async def add_projects(project: Annotated[SProjectAdd, Depends()]):
    projects.append(project)
    return {"ok":"True"}


@router.get("/projects/{project_id}", tags=["Projects"])
def get_projects(projects_id: int):
    return {"data": projects[projects_id-1]}

@router.delete("/projects/{project_id}",tags=["Projects"])
def delete_projects(projects_id: int):
    projects.pop(projects_id-1)
    return {"delete": "True"}


@router.post("/columns/{columns_id}", tags=["Columns"])
async def add_projects(column: Annotated[SColumnsAdd, Depends()]):
    columns.append(column)
    return {"ok":"True"}


@router.get("/columns/{columns_id}", tags=["Columns"])
def get_projects(columns_id: int):
    return {"data": columns[columns_id-1]}

@router.delete("/columns/{columns_id}",tags=["Columns"])
def delete_projects(columns_id: int):
    columns.pop(columns_id-1)
    return {"delete": "True"}



@router.post("/columns/{columns_id}/tasks", tags=["Tasks"])
async def add_tasks(task: Annotated[STaskAdd, Depends()]):
    tasks.append(task)
    return {"ok":"True"}


@router.get("/columns/{columns_id}/tasks", tags=["Tasks"])
def get_tasks(columns_id: int):
    return {"data": tasks[columns_id-1]}

@router.delete("/columns/{columns_id}/tasks",tags=["Tasks"])
def delete_tasks(columns_id: int):
    tasks.pop(columns_id)
    return {"delete": "True"}

@router.post("/columns/{columns_id}/tasks", tags=["Tasks"])
async def add_tasks(task: Annotated[STaskAdd, Depends()]):
    tasks.append(task)
    return {"ok":"True"}


@router.get("/columns/{columns_id}/tasks", tags=["Tasks"])
def get_tasks(columns_id: int):
    return {"data": tasks[columns_id-1]}

@router.delete("/columns/{columns_id}/tasks",tags=["Tasks"])
def delete_tasks(columns_id: int):
    tasks.pop(columns_id-1)
    return {"delete": "True"}

app.include_router(router)