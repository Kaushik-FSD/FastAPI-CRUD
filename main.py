from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import tasks

app = FastAPI()

# --- Custom Exception ---
class TaskException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(TaskException)
def task_exception_handler(request: Request, exc: TaskException):
    return JSONResponse(status_code=400, content={"error": exc.message})

# --- Register Routers ---
app.include_router(tasks.router)