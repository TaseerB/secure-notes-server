from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.task import TaskCreate, TaskRead
from app.schemas.user import UserCreate, UserRead
from app.services.task_service import create_task, list_tasks
from app.services.user_service import create_user, get_users
from app.db.session import get_db
from app.utilities.password_utility import hash_password
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
async def create(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Hash the password before creating the user
        user.password = hash_password(user.password)
        return await create_user(db, user)
    
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Database integrity error creating user: {str(e)}")
        
        # Check if it's a unique constraint violation (duplicate email)
        if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database constraint violation"
            )
    
    except ValueError as e:
        logger.error(f"Invalid input data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid input: {str(e)}"
        )
    
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user"
        )

@router.get("/", response_model=List[UserRead])
async def read_all(db: Session = Depends(get_db)):
    try:
        return await get_users(db)
    
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching users"
        )

# ----------------------------
# Create and get Task per User
# ----------------------------
@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    try:
        return await list_tasks(db, user_id=user_id)
    except Exception as e:
        logger.error(f"Error fetching tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching tasks"
        )
    

@router.post("/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_user_task(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    try:
        return await create_task(db, task, user_id=user_id)
    except Exception as e:
        logger.error(f"Error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task"
        )
