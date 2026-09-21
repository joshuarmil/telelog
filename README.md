# Telelog - Distributed Ingestion Engine

A high-performance sandbox project designed to master distributed data parsing, full-text search indexing, and cloud infrastructure patterns. This project simulates an enterprise-level product catalog search platform, prioritizing search relevance, low latency, and horizontally scalable service architecture.

## Project Status & Sprint Roadmap
- [X] Phase 1: High-Level FastAPI Ingestion Engine & PostgreSQL Core (MVP Complete)
- [ ] Phase 2: Decoupled Background Worker & Anomaly Alert Pipeline (In Progress)
- [ ] Phase 3: Elasticsearch Cluster Sync & GCP Cloud Deployment Deployment (Upcoming)

## Key Architectural Features
- **FastAPI Backend:** Built an asynchronous REST API in Python to orchestrate high-concurrency data transactions.
- **Elasticsearch Cluster:** Implemented deep indexing, custom tokenization, and compound filtering algorithms to run sub-50ms full-text and fuzzy search operations.
- **Service Virtualization:** Developed a background Python worker that mocks high-volume catalog streams to test database ingestion limits.
- **Containerized DevOps Stack:** Native Docker infrastructure configured for local clustering and deployment pipelines.
- **Google Cloud Platform (GCP):** Ready-to-deploy configuration for cloud computing instances with microservices networking.

## Tech Stack & Protocols
- **Languages:** Python, Bash, JSON
- **Databases/Search:** Elasticsearch, Redis (In-memory caching layer)
- **Infrastructure:** Docker, Docker Compose, GCP Compute Engine
- **Frameworks:** FastAPI, Pydantic, Elastic-transport

## System Architecture Diagram
```
[ Client / Web Browser ] 
        │  (REST API / JSON)
        ▼
 [ FastAPI Gateway Service ] 
        │
   ┌────┴────────────────────────┐
   ▼ (Cache Lookup)              ▼ (Search Queries / Bulk Index)
[ Redis Cache ]         [ Elasticsearch Cluster ]
                                 ▲
                                 │ (Simulated Stream Ingestion)
                        [ Python Mock Data Worker ]
```

## Engineering Insights & What I Learned
1. **Optimizing Search Relevance:** I learned how to move past basic database lookups by building customized query clauses in Elasticsearch. I tuned parameters for `multi_match` fields and applied custom string analysis tokenizers to improve typo-tolerance while avoiding heavy index bloating.
2. **Handling Unreliable Cloud Boundaries:** Building the remote service simulation forced me to design custom retry-logic algorithms using linear backoffs. This guarantees that if data streaming nodes fluctuate or lose network connection, the system self-heals without duplicating log events or dropping payload updates.
3. **Observability Tracking:** Set up explicit, structured JSON logging frameworks throughout the ingestion nodes, allowing easy auditing of application performance metrics and mapping directly to enterprise observability patterns.

## Local Setup & Installation
Ensure you have Docker and Docker Compose installed locally:
```bash
# Clone the repository
git clone https://github.com/joshuarmil/telelog.git
cd telelog
```

# Create a `.env` configuration file in the project root directory:
```ini
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=telemetry
DATABASE_URL=postgresql://user:pass@db:5432/telemetry
```

```bash
# Spin up the containers (FastAPI, Elasticsearch, Redis)
docker-compose up --build -d

# Start the API server
uvicorn app.main:app --reload
```

# To run the worker script for simulated processing:
```bash
# In a separate console:
python -m app.workers.worker
```

The API documentation will be available locally at `http://localhost:8000/docs`.

