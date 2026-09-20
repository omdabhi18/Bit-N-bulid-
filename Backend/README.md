# KrishiNetra AI (કૃષિનેત્ર AI) — Backend Platform
### Autonomous Farm-to-Field Advisory & Action Orchestration Agent

Production-grade modular-monolith backend built with **Python**, **FastAPI**, **SQLAlchemy**, **LangGraph-pattern Multi-Agent Orchestration**, **Mock IoT & MQTT Integration**, and **Real-Time WebSockets**.

---

## 🌾 Project Architecture

```
Backend/
├── app/
│   ├── main.py                  # FastAPI Lifespan, WebSocket, CORS & Exception Handlers
│   ├── config.py                # Environment configuration (Pydantic Settings)
│   ├── database.py              # Async SQLAlchemy Engine & Session Maker
│   ├── dependencies.py          # JWT Authentication & DB Session Injection
│   ├── models/                  # 14 SQLAlchemy ORM Models (Farm, Field, Crop, Sensor, Risk, etc.)
│   ├── schemas/                 # Pydantic v2 Request/Response validation schemas
│   ├── api/                     # 17 REST API Routers
│   ├── services/                # Business domain logic layer
│   ├── agents/                  # 11-Agent Cooperative Network & Constraint Engine
│   ├── integrations/            # MQTT, Mock IoT, WebSockets, Weather & Market Providers
│   ├── workers/                 # Periodic telemetry background scheduler
│   └── utils/                   # Structured JSON logger, security & GreenValley farm seeder
├── tests/                       # Complete Pytest test suite (unit, integration & E2E)
├── docs/
│   └── frontend-backend-contract.md # Complete component-to-API contract mapping
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## 🚀 Quick Setup & Running Locally

### 1. Install Dependencies
Ensure you have Python 3.10+ installed:
```bash
cd Backend
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(By default, it runs SQLite `sqlite+aiosqlite:///./krishinetra.db` with Mock IoT enabled for instant zero-dependency local execution).*

### 3. Run the Backend Dev Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- **API Base**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **WebSocket Endpoint**: `ws://localhost:8000/ws/farm/farm-greenvalley-01`

---

## 🧪 Running Tests
Run the comprehensive test suite:
```bash
cd Backend
pytest -v tests/
```

---

## 🐳 Docker Deployment
To run with PostgreSQL, Redis, and Mosquitto MQTT broker:
```bash
cd Backend
docker-compose up --build -d
```

---

## 🤖 The 11 Autonomous Specialized Agents

1. **Master Orchestrator Agent**: Coordinates the entire network, synthesizes multi-agent consensus, and records audit trails.
2. **Soil & Moisture Agent**: Analyzes FDR probe moisture deficit and root wilting thresholds.
3. **Meteorological Agent**: Scans 24-hr rain probabilities and calculates safe agricultural spray windows.
4. **Crop Phenology & Health Agent**: Evaluates flowering stage sensitivity and growth degree days.
5. **Pest & Pathogen Vision Agent**: Cross-references ambient nocturnal humidity with regional outbreak alerts.
6. **Disease Diagnostics Agent**: Multi-spectral and pattern pathology classifier.
7. **Nutrient & NPK Agent**: Analyzes available nitrogen, phosphorus, and potassium levels.
8. **APMC Mandi & Market Agent**: Evaluates spot price arbitrage and optimal selling windows.
9. **Risk Assessment Agent**: Computes deterministic multi-factor risk matrices.
10. **Constrained Action Planner**: Constraint engine enforcing budget ceilings, rain safety, and water supply checks.
11. **Execution & Feedback Agent**: Triggers physical or mock IoT solenoid valves and tracks completion.

---

## 🚜 Complete Demo Scenario (End-to-End)

1. **Moisture Drop**: Field A soil moisture reaches ~31.4% (below 35% target).
2. **Detection**: Soil Agent alerts water stress; Crop Agent notes high vulnerability during flowering.
3. **Constraint Check**: Weather Agent confirms only 12% rain chance; Constraint Engine validates cost (₹45 <= ₹150 budget).
4. **Orchestration**: Orchestrator releases **Action Plan #PLAN-1024** and **Advisory #adv-01**.
5. **Farmer Approval**: Farmer clicks approve (`POST /api/action-plans/PLAN-1024/approve`).
6. **Valve Trigger**: Execution Agent sends MQTT command and activates Solenoid Valve SV-01 (`POST /api/sensors/valve/trigger`).
7. **Absorption Feedback**: Mock IoT simulator runs irrigation for 35 mins; soil moisture normalizes to 46.2% (Optimal).
8. **Real-Time Update**: Live WebSockets push telemetry updates to the frontend dashboard with full activity logs.
