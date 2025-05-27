from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from typing import List
import crud
import schemas

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=List[schemas.Project])
async def list_projects(db: AsyncSession = Depends(get_db)):
    return await crud.get_projects(db)

@router.post("/", response_model=schemas.Project)
async def create_project(project: schemas.ProjectCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_project(db, project)

@router.post("/{project_id}/users/")
async def add_user(project_id: int, user: schemas.ProjectUserBase, db: AsyncSession = Depends(get_db)):
    return await crud.add_user_to_project(db, project_id, user.username)

@router.delete("/{project_id}/users/")
async def remove_user(project_id: int, user: schemas.ProjectUserBase, db: AsyncSession = Depends(get_db)):
    success = await crud.remove_user_from_project(db, project_id, user.username)
    return {"success": success}