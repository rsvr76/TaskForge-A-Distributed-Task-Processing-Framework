import threading
from typing import Dict, Optional
from taskforge.models.task import Task, TaskStatus


class TaskRegistry:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._lock = threading.Lock()

    def add_task(self, task: Task) -> None:
        with self._lock:
            self._tasks[task.task_id] = task

    def get_task(self, task_id: str) -> Optional[Task]:
        with self._lock:
            return self._tasks.get(task_id)

    def update_task_status(self, task_id: str, status: TaskStatus, result: Optional[dict] = None, error_message: Optional[str] = None) -> bool:
        with self._lock:
            if task_id not in self._tasks:
                return False

            task = self._tasks[task_id]
            task.status = status
            task.result = result
            task.error_message = error_message

            if status == TaskStatus.RUNNING and not task.started_at:
                task.started_at = task.created_at
            elif status in (TaskStatus.COMPLETED, TaskStatus.FAILED) and not task.completed_at:
                task.completed_at = task.created_at

            return True

    def store_result(self, task_id: str, result: dict) -> bool:
        with self._lock:
            if task_id not in self._tasks:
                return False

            self._tasks[task_id].result = result
            return True

    def get_all_tasks(self) -> Dict[str, Task]:
        with self._lock:
            return self._tasks.copy()
