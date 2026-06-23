import queue
from taskforge.models.task import Task


class QueueManager:
    def __init__(self):
        self._queue = queue.Queue()

    def enqueue(self, task: Task) -> None:
        self._queue.put(task)

    def dequeue(self) -> Task:
        return self._queue.get()

    def queue_size(self) -> int:
        return self._queue.qsize()

    def is_empty(self) -> bool:
        return self._queue.empty()
