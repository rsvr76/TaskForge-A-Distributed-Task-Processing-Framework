from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid

from taskforge.api.routes import router
from taskforge.core.queue_manager import QueueManager
from taskforge.core.task_registry import TaskRegistry
from taskforge.models.task import Task, TaskStatus

app = FastAPI(title="TaskForge")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

queue_manager = QueueManager()
task_registry = TaskRegistry()

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "TaskForge running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "queue_size": queue_manager.queue_size(),
        "tasks_in_registry": len(task_registry.get_all_tasks())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
