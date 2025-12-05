from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Task
class TaskCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

    