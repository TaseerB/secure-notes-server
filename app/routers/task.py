from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import (
    get_task,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


# @router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
# async def create_task_endpoint(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
#     return await create_task(db, payload)

# @router.get("/", response_model=List[TaskRead])
# async def list_tasks_endpoint(
#     user_id: int,  # Changed from Optional[int] to required
#     skip: int = 0,
#     limit: int = 100,
#     db: AsyncSession = Depends(get_db),
# ):
#     return await list_tasks(db, user_id=user_id, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_endpoint(task_id: int, db: AsyncSession = Depends(get_db)):
    return await get_task(db, task_id)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task_endpoint(task_id: int, payload: TaskUpdate, db: AsyncSession = Depends(get_db)):
    return await update_task(db, task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(task_id: int, db: AsyncSession = Depends(get_db)):
    await delete_task(db, task_id)