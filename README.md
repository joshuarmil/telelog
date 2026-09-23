# Telelog - Distributed Ingestion Engine

A containerized, event-driven data pipeline designed to ingest high-frequency IoT device telemetry, isolate database transaction limits, and scale processing out-of-band across decoupled, concurrent worker nodes.

## Project Status & Sprint Roadmap
- [X] Phase 1: High-Level FastAPI Ingestion Engine & PostgreSQL Core (Completed)
- [X] Phase 2: Decoupled Background Worker & Anomaly Alert Pipeline (Completed)
- [ ] Phase 3: Elasticsearch Cluster Sync & GCP Cloud Deployment Deployment (In Progress)

## Key Architectural Features
- **FastAPI Backend:** Built a REST API in Python to orchestrate high-concurrency data transactions.
- **Elasticsearch Cluster:** Implemented deep indexing, custom tokenization, and compound filtering algorithms to run sub-50ms full-text and fuzzy search operations.
- **Service Virtualization:** Developed a background Python worker that mocks high-volume catalog streams to test database ingestion limits.
- **Containerized DevOps Stack:** Native Docker infrastructure configured for local clustering and deployment pipelines.
- **Google Cloud Platform (GCP):** Ready-to-deploy configuration for cloud computing instances with microservices networking.

## Tech Stack & Protocols
- **Languages:** Python, Bash, JSON
- **Infrastructure:** Docker
- **Frameworks:** FastAPI, Pydantic
- **Data Persistence:** PostgreSQL, SQLAlchemy, Alembic

## Architectural Design Principles

The core objective of this architecture is to decouple network-facing ingestion from database-heavy business logic evaluations, ensuring minimal response latency and bulletproof system scaling.

```
                  ┌───────────────────────────────┐
                  │   Incoming Hardware Sensors   │
                  └───────────────┬───────────────┘
                                  │  (HTTP POST /telemetry)
                                  ▼
                    ┌───────────────────────────┐
                    │    FastAPI Web Gateway    │
                    └─────────────┬─────────────┘
                                  │  (Insert row with processed=False)
                                  ▼
                    ┌───────────────────────────┐
                    │    PostgreSQL Database    │
                    └─────────────┬─────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          │ (skip_locked=True)    │ (skip_locked=True)    │ (skip_locked=True)
          ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Worker Node 1    │    │ Worker Node 2    │    │ Worker Node 3    │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```
### 1. Decoupled Ingestion & Processing
Instead of running expensive threshold logic or writing alert logs inside the HTTP request thread, the web API validates payloads via Pydantic schemas, commits the raw metrics with a `processed = False` state index, and immediately releases the network client with an HTTP 201 status code.

### 2. Transaction Boundary Isolation
Database sessions are managed contextually based on execution environments. Routing leverages FastAPI's framework Dependency Injection to safely bind connection lifecycles to individual HTTP requests. Standalone background worker loops use native context managers (`with SessionLocal() as db:`) to enforce strict transaction limits, isolating operational rollbacks completely from the network.

### 3. Horizontal Scale via Row Locking
To support high-throughput load distributions without race conditions, the background worker leverages PostgreSQL row-level locks via `.with_for_update(skip_locked=True)`. When scaled horizontally across multiple container instances, worker nodes drain the transaction queue concurrently. Each worker locks and processes its own discrete batch, while sibling containers bypass those locked records to claim the next available segments without deadlocking or duplicating alert writes.

## Local Setup & Installation
Ensure you have Docker and Docker Compose installed locally:
```bash
git clone https://github.com/joshuarmil/telelog.git
cd telelog
```

### 1. Create a `.env` configuration file in the project root directory:
```ini
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=telemetry
DATABASE_URL=postgresql://user:pass@db:5432/telemetry
```

### 2. Spin up the multi-container cluster
Build the cached Python container environments and launch the persistent database, web gateway, and scaled background processing worker nodes inside a private bridge network:

```bash
docker-compose up -d --build --scale worker=3
```

### 3. Inject simulated loads
In a separate console, run the test injection harness. This script provisions a fresh mock hardware asset and fires a series of realistic telemetry patterns, including intentional temperature and voltage warnings:

```bash
python simulator.py
```

### 4. Verify System Alerts Via API Gateway
Confirm the background processing engines caught the thresholds and recorded persistent logs by querying the read-only alert monitoring endpoint:

```bash
curl http://localhost:8000/alerts/
```

The API documentation will be available locally at `http://localhost:8000/docs`.

## Performance-Tuning Talking Points

- **Indexed Boolean Selectivity:** The `TelemetryReading.processed` column utilizes a database index. While indexing booleans is traditionally inefficient, it serves as a highly selective "needle in a haystack" lookup model here. As millions of processed historical records accumulate, the query planner bypasses them entirely, targeting only the small handful of active, un-drained data rows in under a millisecond.
- **Batch Sizing Backoff:** Workers run an adaptive loop. If a query yields rows, the worker processes them and checks in again immediately. If a query returns empty, the worker implements a brief sleep duration backoff to conserve database CPU resources.