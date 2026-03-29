from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# --- Models ---

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
    id: int
    title: str
    completed: bool
    priority: int

# --- Fake DB ---

fake_db: dict = {}
counter: int = 0

# --- Custom Exception ---

class TaskException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(TaskException)
def task_exception_handler(request: Request, exc: TaskException):
    return JSONResponse(status_code=400, content={"error": exc.message})

# --- Dependencies ---

def pagination(page: int = 1, limit: int = 10):
    return {"page": page, "limit": limit}

# --- Routes ---

@app.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks(params: dict = Depends(pagination)):
    return list(fake_db.values())

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return fake_db[task_id]

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global counter
    counter += 1
    new_task = {"id": counter, "title": task.title, "completed": task.completed, "priority": task.priority}
    fake_db[counter] = new_task
    return new_task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate):
    if task_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    updated = {"id": task_id, "title": task.title, "completed": task.completed, "priority": task.priority}
    fake_db[task_id] = updated
    return updated

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    del fake_db[task_id]