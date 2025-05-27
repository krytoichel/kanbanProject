from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
import crud
import schemas
from typing import List
from typing import Optional

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, task)

@router.get("/column/{column_id}", response_model=List[schemas.Task])
async def list_tasks(
    column_id: int,
    title: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_tasks_by_column(db, column_id, title)

@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    updated = await crud.update_task(db, task_id, task.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}