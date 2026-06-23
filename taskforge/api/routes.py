from fastapi import FastAPI, HTTPException, Depends
from fastapi.routing import APIRouter
from pydantic import BaseModel
import uuid
from taskforge.models.task import Task, TaskStatus
from taskforge.core.queue_manager import QueueManager
from taskforge.core.task_registry import TaskRegistry
from taskforge.core.worker import Worker

router = APIRouter()

queue_manager = QueueManager()
task_registry = TaskRegistry()

workers = []
for i in range(4):
    worker = Worker(i + 1, queue_manager, task_registry)
    worker.start()
    workers.append(worker)


class CreateTaskRequest(BaseModel):
    task_type: str
    payload: dict


@router.post("/tasks")
async def create_task(request: CreateTaskRequest):
    task_id = str(uuid.uuid4())

    if request.task_type not in ["sleep", "sum", "fail"]:
        raise HTTPException(status_code=400, detail=f"Unknown task type: {request.task_type}")

    task = Task(task_id=task_id, task_type=request.task_type, payload=request.payload)
    task_registry.add_task(task)
    queue_manager.enqueue(task)

    return {"task_id": task_id, "status": task.status.value}


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task = task_registry.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task.to_dict()


@router.get("/tasks/{task_id}/result")
async def get_task_result(task_id: str):
    task = task_registry.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != TaskStatus.COMPLETED:
        raise HTTPException(status_code=400, detail=f"Task not completed. Status: {task.status.value}")

    return task.to_dict()
