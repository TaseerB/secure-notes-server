from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# Pydantic v1/v2 compatibility for ORM mode/from_attributes
try:
    from pydantic import ConfigDict

    class ORMModel(BaseModel):
        model_config = ConfigDict(from_attributes=True)
except Exception:
    class ORMModel(BaseModel):
        class Config:
            orm_mode = True


class TaskBase(BaseModel):
    name: str
    content: Optional[str] = None


class TaskCreate(TaskBase):
    # user_id will be provided as a path parameter in your endpoint, not in the request body
    pass


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None


class TaskRead(ORMModel):
    id: int
    user_id: int
    name: str
    content: Optional[str] = None
    created_at: datetime
    updated_at: datetime