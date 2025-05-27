from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
import crud
from typing import List
import schemas

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/{task_id}")
async def add_log(task_id: int, message: str, db: AsyncSession = Depends(get_db)):
    return await crud.create_task_log(db, task_id, message)

@router.get("/{task_id}", response_model=List[schemas.TaskLog])
async def get_logs(task_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_logs_for_task(db, task_id)