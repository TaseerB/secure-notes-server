from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool = True


class UserRead(UserCreate):
    id: int

    class Config:
        orm_mode = True
