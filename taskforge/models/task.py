from datetime import datetime
from typing import Any, Optional
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task:
    def __init__(
        self,
        task_id: str,
        task_type: str,
        payload: dict,
        status: TaskStatus = TaskStatus.PENDING,
        result: Optional[Any] = None,
        error_message: Optional[str] = None
    ):
        self.task_id = task_id
        self.task_type = task_type
        self.payload = payload
        self.status = status
        self.result = result
        self.error_message = error_message
        self.created_at = datetime.utcnow()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "payload": self.payload,
            "status": self.status.value,
            "result": self.result,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task = cls(
            task_id=data["task_id"],
            task_type=data["task_type"],
            payload=data["payload"],
            status=TaskStatus(data["status"]),
            result=data.get("result"),
            error_message=data.get("error_message")
        )
        task.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("started_at"):
            task.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            task.completed_at = datetime.fromisoformat(data["completed_at"])
        return task
