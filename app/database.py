from typing import Optional
from app.models import TaskResponse

# This acts as our fake database
fake_db: dict[int, dict] = {}
counter: int = 0

def get_all() -> list[dict]:
    return list(fake_db.values())

def get_by_id(task_id: int) -> Optional[dict]:
    return fake_db.get(task_id)  # returns None if not found

def create(data: dict) -> dict:
    global counter
    counter += 1
    data["id"] = counter
    fake_db[counter] = data
    return data

def update(task_id: int, data: dict) -> Optional[dict]:
    if task_id not in fake_db:
        return None
    data["id"] = task_id
    fake_db[task_id] = data
    return data

def delete(task_id: int) -> bool:
    if task_id not in fake_db:
        return False
    del fake_db[task_id]
    return True