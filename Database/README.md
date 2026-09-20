# 🌾 KrishiNetra AI – Production Database Architecture

Welcome to the production-ready **Database Layer** for **KrishiNetra AI – Autonomous Farm-to-Field Advisory & Action Orchestration Platform** (GreenValley Smart Farms, Rajkot, Gujarat).

This package provides a high-performance, robust, and ACID-compliant relational persistence layer designed for PostgreSQL (with zero-configuration SQLite fallback for instant development and testing), integrated via SQLAlchemy 2.0 async ORM, Alembic migrations, Pydantic v2 schemas/DTOs, and the Repository Pattern.

---

## 📁 Directory Structure

```tree
Database/
├── config.py                 # DB & connection pool configuration (PostgreSQL + SQLite fallback)
├── connection.py             # Async & sync SQLAlchemy engines, SessionLocal, ping utility
├── requirements.txt          # Python dependencies for the database layer
├── README.md                 # Documentation and operational runbook
├── docs/
│   ├── database-integration-plan.md     # Architectural audit & integration strategy document
│   └── frontend-database-contract.md    # Frontend UI -> API -> Service -> DB mapping table
├── models/                   # 18 Domain Models (SQLAlchemy Declarative Base)
│   ├── __init__.py           # Model index & Base registry
│   ├── user.py               # Users, Farmer, Expert, Admin RBAC
│   ├── farm.py               # Farms (Acreage, location, soil type)
│   ├── field.py              # Fields (Geo-coordinates, polygon boundary, status)
│   ├── crop.py               # Crops (Phenology stage, sowing/harvest dates)
│   ├── sensor.py             # IoT Sensors (Soil, Temp, pH, NPK, Valves)
│   ├── sensor_reading.py     # High-throughput time-series telemetry with composite indexes
│   ├── weather_data.py       # Weather observations & microclimate forecasts
│   ├── market_price.py       # APMC Mandi market prices & arbitrage recommendations
│   ├── risk.py               # Detected risks (Water stress, pests, disease, nutrients)
│   ├── ai_advisory.py        # Explainable AI recommendations & reasoning
│   ├── action_plan.py        # Orchestrated action plans & constraint validation
│   ├── task.py               # Dispatched Kanban field execution tasks
│   ├── disease_analysis.py   # Computer-vision leaf disease diagnostic records
│   ├── expert_request.py     # Agronomist escalation review tickets
│   ├── agent_run.py          # Execution telemetry for all 11 autonomous agents
│   ├── alert.py              # Real-time farmer push alerts
│   ├── notification.py       # Multi-channel notifications (Web, SMS, WhatsApp)
│   └── activity_log.py       # Immutable chronological orchestration audit trail
├── schemas/                  # Clean Pydantic v2 Data Transfer Objects (DTOs)
│   ├── __init__.py
│   └── dtos.py               # Request, Response, and Pagination DTO schemas
├── repositories/             # Isolated Repository Pattern (Data Access Layer)
│   ├── __init__.py
│   ├── base_repository.py    # Generic asynchronous CRUD repository
│   ├── user_repository.py    # User querying by email, phone, role
│   ├── farm_repository.py    # Farm & field relationship retrieval
│   ├── sensor_repository.py  # Time-series telemetry insertion & windowed pagination
│   ├── risk_repository.py    # Risk aggregation & status updates
│   ├── action_plan_repository.py # Atomic approval & auto-task dispatch transaction
│   ├── task_repository.py    # Task state-machine updates & completion logging
│   └── activity_log_repository.py # Chronological immutable audit trail logging
├── migrations/               # Alembic database migration management
│   ├── alembic.ini           # Alembic configuration
│   ├── env.py                # Migration environment loading all 18 models
│   ├── script.py.mako        # Migration template
│   └── versions/
│       └── 001_initial_schema.py # Initial migration creating all 18 tables & indexes
├── scripts/                  # Utilities & Database Seeders
│   ├── schema.sql            # Pure PostgreSQL DDL script with all tables & constraints
│   ├── init_db.py            # Automated table initialization verification script
│   └── seed_data.py          # Seed script with GreenValley Smart Farms demo data
├── docker/                   # Container orchestration
│   ├── docker-compose.yml    # PostgreSQL 15, Redis 7, Mosquitto MQTT broker
│   └── init.sql              # Container startup initialization extensions
└── tests/                    # 100% Passing Automated Test Suite
    ├── conftest.py           # In-memory async SQLite engine & session fixtures
    ├── test_connection.py    # Database connection & healthcheck validation
    ├── test_models.py        # All 18 SQLAlchemy models instantiation & relationship tests
    ├── test_repositories.py  # Base and custom repository CRUD test suite
    ├── test_transactions.py  # ACID rollback and atomic approval transaction tests
    └── test_e2e_db_flow.py   # Sensor -> Risk -> Plan -> Approval -> Task -> Log pipeline
```

---

## 🚀 Quickstart & Usage

### 1. Requirements Installation
```bash
pip install -r Database/requirements.txt
```

### 2. Running Automated Tests
The test suite executes 18 automated tests across connection, models, repositories, ACID transactions, and the complete end-to-end pipeline:
```bash
python -m pytest -v Database/tests/
```

### 3. Initializing Database Schema
Run the schema initializer to verify connection and generate all 18 tables:
```bash
python Database/scripts/init_db.py
```

### 4. Seeding Demo Data (GreenValley Smart Farms)
Populate all 18 entities with consistent agronomic data (Kishanbhai Patel, Rajkot, Gujarat):
```bash
python Database/scripts/seed_data.py
```

---

## 🐘 PostgreSQL & Docker Compose Setup

To start local production services (PostgreSQL 15, Redis 7, Eclipse Mosquitto MQTT):

```bash
cd Database/docker
docker-compose up -d
```

Configure your environment:
```env
DATABASE_URL=postgresql+asyncpg://krishinetra_user:krishinetra_secret_pass@localhost:5432/krishinetra_db
REDIS_URL=redis://localhost:6379/0
```

### Running Alembic Migrations
```bash
# Apply migrations to the latest revision
alembic -c Database/migrations/alembic.ini upgrade head

# Roll back the last migration if needed
alembic -c Database/migrations/alembic.ini downgrade -1
```

---

## 🛡️ ACID Transaction Safety: Action Plan Approval

When a farmer approves an action plan via the dashboard, `ActionPlanRepository.approve_and_dispatch_task`:
1. Validates plan constraints and existence.
2. Updates `ActionPlan.status` to `APPROVED`.
3. Atomically generates a dispatched `Task` assigned to the farmer/worker.
4. Appends an immutable `ActivityLog` audit record.
5. Commits atomically or rolls back with zero orphan records if any step fails.
