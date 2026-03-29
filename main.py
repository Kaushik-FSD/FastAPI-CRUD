from fastapi import FastAPI
# Pydantic models to define and validate that data.
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False

@app.get('/tasks')
def get_all_tasks():
    return {"tasks": []}

@app.get('/tasks/{task_id}')
def get_task_by_id(task_id: int):
    return {"task_id" : task_id}

@app.get("/tasks")
def get_tasks(completed: bool = False):
    return {"completed": completed}

@app.post("/tasks")
def create_task(task: Task):
    return task
