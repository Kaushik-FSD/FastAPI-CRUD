from fastapi import FastAPI, status
# Pydantic models to define and validate that data.
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Tag(BaseModel):
    name: str
    color: str = "blue"

# We can have multiple validation like zod
# Input model — what client sends
class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    completed: bool = False
    priority: int = Field(default=1, ge=1, le=5)  # between 1 and 5
    tag: Optional[Tag] = None  # nested model

# Response model — what client gets back
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    priority: int

@app.get('/task')
def get_all_tasks():
    return {"tasks": []}

# This is for dynamic path
@app.get('/tasks/{task_id}')
def get_task_by_id(task_id: int):
    return {"task_id" : task_id}

# This is for query params e.g: /tasks?completed=<something>
@app.get("/tasks")
def get_tasks(completed: bool = False):
    return {"completed": completed}

# @app.post("/tasks", response_model=TaskResponse)
# def create_task(task: TaskCreate):
#     # return task
#     # simulate saving and getting back an id
#     return {"id": 1, "title": task.title, "completed": task.completed, "priority": task.priority}

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    # return task
    # simulate saving and getting back an id
    return {"id": 1, "title": task.title, "completed": task.completed, "priority": task.priority}

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    return None  # 204 means no content returned
