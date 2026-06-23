import threading
import time
from taskforge.services.task_executor import TaskExecutor
from taskforge.core.task_registry import TaskRegistry
from taskforge.core.queue_manager import QueueManager
from taskforge.models.task import Task, TaskStatus


class Worker(threading.Thread):
    def __init__(self, worker_id: int, queue_manager: QueueManager, task_registry: TaskRegistry):
        super().__init__()
        self.worker_id = worker_id
        self.queue_manager = queue_manager
        self.task_registry = task_registry
        self._stop_event = threading.Event()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                if self.queue_manager.is_empty():
                    time.sleep(0.1)
                    continue

                task = self.queue_manager.dequeue()
                self.task_registry.update_task_status(task.task_id, TaskStatus.RUNNING)

                try:
                    result = TaskExecutor.execute_task(task)
                    self.task_registry.update_task_status(task.task_id, TaskStatus.COMPLETED, result=result)
                except Exception as e:
                    self.task_registry.update_task_status(task.task_id, TaskStatus.FAILED, error_message=str(e))

            except Exception as e:
                print(f"Worker {self.worker_id} error: {e}")

    def stop(self) -> None:
        self._stop_event.set()
