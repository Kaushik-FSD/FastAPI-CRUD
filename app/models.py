from pydantic import BaseModel, Field
from typing import Optional

class Tag(BaseModel):
    name: str
    color: str = "blue"

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    completed: bool = False
    priority: int = Field(default=1, ge=1, le=5)
    tag: Optional[Tag] = None

class TaskResponse(BaseModel):
    model_config = {"extra": "allow"}
    id: int
    title: str
    completed: bool
    priority: int