# TaskForge

TaskForge is a task processing system that enables asynchronous execution of background jobs across multiple worker threads.

## Project Structure

```
taskforge/
├── app.py
├── api/
│   └── routes.py
├── core/
│   ├── queue_manager.py
│   ├── worker.py
│   └── task_registry.py
├── models/
│   └── task.py
├── services/
│   └── task_executor.py
├── tests/
├── requirements.txt
└── README.md
```

## Architecture

```
            Client
               │
               ▼
         FastAPI Server
               │
               ▼
          Task Queue
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
Worker 1   Worker 2   Worker 3
    │          │          │
    └──────────┼──────────┘
               ▼
         Result Storage
```

## Task Lifecycle

PENDING → RUNNING → COMPLETED or FAILED

## Supported Task Types

- **sleep**: Sleep for N seconds
- **sum**: Sum a list of numbers
- **fail**: Intentionally fail to test error handling

## API Endpoints

### Create Task

POST /tasks

Request:
```json
{
  "task_type": "sleep",
  "payload": {
    "seconds": 5
  }
}
```

Response:
```json
{
  "task_id": "abc123",
  "status": "PENDING"
}
```

### Get Task Status

GET /tasks/{task_id}

Response:
```json
{
  "task_id": "abc123",
  "status": "RUNNING"
}
```

### Get Task Result

GET /tasks/{task_id}/result

Response:
```json
{
  "task_id": "abc123",
  "result": {
    ...
  }
}
```

### Health Check

GET /health

Response:
```json
{
  "status": "healthy"
}
```

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

## Testing

Run tests:
```bash
pytest
```

## Future Roadmap

Phase 2 may include:
- Database persistence
- Auto-scaling worker pool
- Advanced retry logic
- Task prioritization
- Monitoring and metrics
