from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_users
from app.db.session import get_db
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(db, user)


@router.get("/", response_model=List[UserRead])
async def read_all(db: Session = Depends(get_db)):
    return await get_users(db)


# @router.post("/", response_model=UserCreate)
# def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
#     return create_user(db, user)


# @router.get("/{user_id}", response_model=UserCreate)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     return get_user_by_id(db, user_id)


# Get All users
# @router.get("/")
# def get_all_users():
#     return [{"username": "user1"}, {"username": "user2"}]
