import time
from typing import Any, Dict
from taskforge.models.task import Task, TaskStatus


class TaskExecutor:
    @staticmethod
    def execute_task(task: Task) -> Dict[str, Any]:
        task_type = task.task_type
        payload = task.payload

        if task_type == "sleep":
            seconds = payload.get("seconds", 1)
            time.sleep(seconds)
            return {"message": f"slept successfully for {seconds} seconds"}

        elif task_type == "sum":
            numbers = payload.get("numbers", [])
            result = sum(numbers)
            return {"sum": result}

        elif task_type == "fail":
            raise Exception("Task failed intentionally")

        else:
            raise ValueError(f"Unknown task type: {task_type}")
