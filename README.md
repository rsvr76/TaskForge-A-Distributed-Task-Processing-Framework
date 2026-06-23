# TaskForge

TaskForge is a distributed task queue designed to process background jobs reliably and efficiently across multiple worker nodes. Inspired by production-grade systems such as Celery, TaskForge demonstrates core distributed systems concepts including concurrency, synchronization, fault tolerance, and asynchronous task execution.

The system enables clients to submit tasks through a REST API, routes them through a Redis-backed message broker, and distributes execution across multiple worker processes. Task status tracking, retry mechanisms, and monitoring capabilities provide reliability for long-running workloads such as machine learning inference and data processing pipelines.

## Key Features
- Distributed task scheduling
- Multi-worker concurrent execution
- Redis-backed message broker
- Task state management
- Automatic retry on failure
- Fault-tolerant processing
- REST API using FastAPI
- Dockerized deployment
- Designed for scalable ML inference workloads

## Technologies
- Python
- FastAPI
- Redis
- PostgreSQL
- Docker
- Threading / Multiprocessing
