import logging
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

logger = logging.getLogger(__name__)


async def create_task(db: AsyncSession, payload: TaskCreate) -> Task:
    data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    task = Task(**data)
    try:
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("DB error creating task: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task",
        )


async def get_task(db: AsyncSession, task_id: int) -> Task:
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


async def list_tasks(
    db: AsyncSession, user_id: Optional[int] = None, skip: int = 0, limit: int = 100
) -> List[Task]:
    stmt = select(Task).order_by(Task.id).offset(skip).limit(limit)
    if user_id is not None:
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.id).offset(skip).limit(limit)
    try:
        result = await db.execute(stmt)
        return result.scalars().all()
    except SQLAlchemyError as e:
        logger.error("DB error listing tasks: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list tasks",
        )


async def update_task(db: AsyncSession, task_id: int, payload: TaskUpdate) -> Task:
    task = await get_task(db, task_id)
    data = payload.model_dump(exclude_unset=True) if hasattr(payload, "model_dump") else payload.dict(exclude_unset=True)

    for field, value in data.items():
        setattr(task, field, value)

    try:
        await db.commit()
        await db.refresh(task)
        return task
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("DB error updating task: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task",
        )


async def delete_task(db: AsyncSession, task_id: int) -> None:
    task = await get_task(db, task_id)
    try:
        await db.delete(task)
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("DB error deleting task: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task",
        )