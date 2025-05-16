from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas, database

app = FastAPI()

# Инициализация БД
@app.on_event("startup")
async def on_startup():
    await database.init_db()

# Зависимость
async def get_db():
    async with database.async_session() as session:
        yield session

@app.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(username=user.username, password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.UserOut)
async def login(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).where(models.User.username == user.username, models.User.password == user.password)
    )
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return existing_user