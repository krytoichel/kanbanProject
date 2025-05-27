from fastapi import FastAPI
from routers import projects, columns, tasks, logs, auth 
from database import engine, Base
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(columns.router, prefix="/columns", tags=["Columns"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])
app.include_router(auth.router)