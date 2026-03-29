from fastapi import APIRouter, HTTPException, Depends, status
from app.models import TaskCreate, TaskResponse
from app import database

router = APIRouter(
    prefix="/tasks",       # all routes here start with /tasks
    tags=["Tasks"]         # groups them in Swagger UI
)

# --- Dependency ---

def pagination(page: int = 1, limit: int = 10):
    return {"page": page, "limit": limit}

# --- Routes ---

@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(params: dict = Depends(pagination)):
    return database.get_all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = database.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    data = task.model_dump()   # converts pydantic model → dict
    return database.create(data)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate):
    data = task.model_dump()
    updated = database.update(task_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return updated

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    deleted = database.delete(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )