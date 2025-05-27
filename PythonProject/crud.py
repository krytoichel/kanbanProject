from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Project, ProjectUser
from schemas import ProjectCreate
from models import ColumnModel
from schemas import ColumnCreate
from sqlalchemy import select
from models import Task
from schemas import TaskCreate
from sqlalchemy import select
from models import TaskLog
from schemas import TaskLog as TaskLogSchema
from sqlalchemy import select
from models import User


# Проект
async def get_projects(db: AsyncSession):
    result = await db.execute(select(Project))
    return result.scalars().all()

async def create_project(db: AsyncSession, project: ProjectCreate):
    db_project = Project(name=project.name)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project

async def add_user_to_project(db: AsyncSession, project_id: int, username: str):
    db_user = ProjectUser(project_id=project_id, username=username)
    db.add(db_user)
    await db.commit()
    return db_user

async def remove_user_from_project(db: AsyncSession, project_id: int, username: str):
    result = await db.execute(select(ProjectUser).where(ProjectUser.project_id == project_id, ProjectUser.username == username))
    user = result.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False

# Колонка
async def create_column(db: AsyncSession, column: ColumnCreate):
    db_column = ColumnModel(**column.dict())
    db.add(db_column)
    await db.commit()
    await db.refresh(db_column)
    return db_column

async def get_columns_by_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(ColumnModel).where(ColumnModel.project_id == project_id))
    return result.scalars().all()

async def update_column(db: AsyncSession, column_id: int, name: str):
    result = await db.execute(select(ColumnModel).where(ColumnModel.id == column_id))
    db_column = result.scalar_one_or_none()
    if db_column:
        db_column.name = name
        await db.commit()
        await db.refresh(db_column)
        return db_column
    return None

async def delete_column(db: AsyncSession, column_id: int):
    result = await db.execute(select(ColumnModel).where(ColumnModel.id == column_id))
    db_column = result.scalar_one_or_none()
    if db_column:
        await db.delete(db_column)
        await db.commit()
        return True
    return False


#Задача
async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    log = TaskLog(task_id=db_task.id, message="Task created")
    db.add(log)
    await db.commit()

    return db_task

async def get_tasks_by_column(db: AsyncSession, column_id: int, title_filter: str = None):
    query = select(Task).where(Task.column_id == column_id)
    if title_filter:
        query = query.where(Task.title.contains(title_filter))
    result = await db.execute(query)
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, data: dict):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task:
        old_column_id = db_task.column_id
        for key, value in data.items():
            setattr(db_task, key, value)
        await db.commit()

        if "column_id" in data and data["column_id"] != old_column_id:
            log_message = f"Task replace from column {old_column_id} in {data['column_id']}"
        else:
            log_message = "Task updated"

        log = TaskLog(task_id=db_task.id, message=log_message)
        db.add(log)
        await db.commit()

        await db.refresh(db_task)
        return db_task
    return None

async def delete_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task:
        await db.delete(db_task)
        await db.commit()
        return True
    return False

#Логи
async def create_task_log(db: AsyncSession, task_id: int, message: str):
    log = TaskLog(task_id=task_id, message=message)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

async def get_logs_for_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(TaskLog).where(TaskLog.task_id == task_id).order_by(TaskLog.created_at))
    return result.scalars().all()