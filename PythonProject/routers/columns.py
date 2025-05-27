from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal
from typing import List
import crud
import schemas

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=schemas.Column)
async def create_column(column: schemas.ColumnCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_column(db, column)

@router.get("/project/{project_id}", response_model=List[schemas.Column])
async def list_columns(project_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_columns_by_project(db, project_id)

@router.put("/{column_id}", response_model=schemas.Column)
async def update_column(column_id: int, name: str, db: AsyncSession = Depends(get_db)):
    column = await crud.update_column(db, column_id, name)
    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")
    return column

@router.delete("/{column_id}")
async def delete_column(column_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_column(db, column_id)
    if not success:
        raise HTTPException(status_code=404, detail="Column not found")
    return {"success": True}