# 🌾 KrishiNetra AI (કૃષિનેત્ર AI)
### Autonomous Farm-to-Field Advisory & Action Orchestration Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.115-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%7C%20Vite-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy%202.0%20Async-D71F00?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2015%20%2F%20SQLite-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![MQTT](https://img.shields.io/badge/IoT-MQTT%20%7C%20Paho-660066?style=flat&logo=eclipse-mosquitto&logoColor=white)](https://mqtt.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white)](https://python.org)

---

## 📖 Executive Summary

**KrishiNetra AI** is a production-grade, closed-loop **autonomous agricultural intelligence and action orchestration platform** built specifically for Indian agriculture. 

Traditional precision-farming tools act as passive dashboards that merely display sensor charts, leaving interpretation, risk evaluation, weather checking, and physical execution entirely to the farmer. **KrishiNetra AI bridges this critical execution gap**:
1. **Continuously ingests** multi-spectral IoT telemetry (soil moisture, temperature, EC, pH, NPK).
2. **Coordinates 11 autonomous, domain-specialized AI agents** using a LangGraph-inspired consensus network.
3. **Validates constrained action plans** against financial budget ceilings, rain safety windows, hydraulic line pressure, and water supplies.
4. **Empowers the farmer** with transparent, explainable recommendations in vernacular languages (**Gujarati**, **Hindi**, and **English**).
5. **Actuates physical field hardware** (solenoid irrigation valves) via MQTT / IoT gateways with real-time feedback and immutable audit logging.

> **Reference Deployment**: GreenValley Smart Farms, Rajkot, Gujarat (Farmer: Kishanbhai Patel; Crops: BT Cotton, Groundnut, Sharbati Wheat).

---

## 🏛️ System Architecture & Data Flow

```mermaid
flowchart TB
    subgraph Edge_IoT["🌾 Edge IoT & Physical Field Devices"]
        S1["FDR Soil Moisture Probes"]
        S2["NPK & Soil Chemistry Sensors"]
        S3["Microclimate Weather Stations"]
        V1["IoT Solenoid Irrigation Valves"]
    end

    subgraph Messaging["⚡ Communication & Event Broker"]
        MQTT["Mosquitto MQTT Broker<br/>(Topics: farm/+/field/+/telemetry | command)"]
        WS["WebSocket Server<br/>(/ws/farm/{farm_id})"]
        Jitter["Telemetry Background Worker<br/>(Drift & Simulation)"]
    end

    subgraph Backend_Platform["🧠 FastAPI Modular-Monolith Platform (Port 8000)"]
        API["17 REST API Routers<br/>(/api/*)"]
        
        subgraph Multi_Agent_Core["🤖 11 Autonomous Cooperative Agents"]
            MO["1. Master Orchestrator"]
            SM["2. Soil & Moisture Agent"]
            MET["3. Meteorological Agent"]
            CP["4. Crop Phenology Agent"]
            PP["5. Pest & Pathogen Vision"]
            DD["6. Disease Diagnostics Agent"]
            NPK["7. Nutrient / NPK Agent"]
            MKT["8. APMC Mandi Agent"]
            RA["9. Risk Assessment Agent"]
            CAP["10. Constrained Action Planner"]
            EXE["11. Execution & Feedback Agent"]
        end

        CE["🛡️ Constraint Engine<br/>(Budget, Weather, Hydraulics, Safety)"]
        XAI["🔍 Explainability Engine<br/>(No Black-Box Reasoning)"]
    end

    subgraph Integration_Layer["🔌 External Integration Providers"]
        OM["Open-Meteo Weather API<br/>(Zero-Config Agro-Met)"]
        LLM["Google Gemini / OpenAI / Mock<br/>(Agricultural Domain Grounding)"]
        MANDI["Agmarknet / OGD Data<br/>(APMC Spot & MSP Pricing)"]
        CLOUD["Cloudinary / S3 / Local<br/>(Plant Pathology Imagery)"]
        VOICE["WebSpeech / Whisper / TTS<br/>(Vernacular Multilingual Voice)"]
    end

    subgraph Data_Layer["💾 Relational & Cache Layer"]
        PG[("PostgreSQL 15 / SQLite<br/>(18 SQLAlchemy Models)")]
        REDIS[("Redis 7<br/>(Rate Cache & Session)")]
        AUDIT[("Immutable Activity Log & Agent Runs")]
    end

    subgraph Frontend_App["💻 React 18 + Vite Modern Dashboard (Port 5173)"]
        UI_DASH["Live Dashboard & Health Score"]
        UI_MAP["GIS Farm Boundary Mapbox"]
        UI_MON["Telemetry Charts & Sensor Fleet"]
        UI_RISK["Risk Matrix & Threat Center"]
        UI_ADV["Explainable AI Recommendations"]
        UI_PLAN["Constrained Action Plans"]
        UI_TASK["Kanban Field Task Execution"]
        UI_AGENTS["Multi-Agent Terminal Stream"]
        UI_DISEASE["Computer Vision Leaf Diagnostics"]
        UI_VOICE["Kisan Multilingual Voice Bot"]
        UI_MANDI["APMC Mandi Price Intelligence"]
    end

    Edge_IoT <-->|Telemetry & Valve Actuation| MQTT
    MQTT --> Backend_Platform
    Backend_Platform <--> Integration_Layer
    Backend_Platform <--> Data_Layer
    Backend_Platform -->|Push Events| WS
    WS --> Frontend_App
    Frontend_App <-->|REST APIs| API
    Jitter -.-> Backend_Platform
```

---

## ⚡ The Autonomous 21-Step Closed-Loop Flow

To guarantee safety and transparency, KrishiNetra executes a deterministic 21-step operational cycle:

```
[Telemetry Ingestion]
  1. IoT FDR sensor measures root-zone soil moisture at 31.4% (Threshold: 35.0%).
  2. Telemetry published to MQTT topic: `farm/farm-greenvalley-01/field/field-a/sensor/SN-Cotton-01/telemetry`.
  3. Sensor worker receives and validates numeric bounds (0-100%).
  4. Telemetry logged into `sensor_readings` table with composite indexes.
  5. WebSocket broadcasts `sensor_update` to connected frontend clients.

[Multi-Agent Deliberation & Risk Assessment]
  6. Soil & Moisture Agent evaluates threshold deficit: 31.4% < 35.0% (-3.6% deficit).
  7. Meteorological Agent scans 24-hr forecast: Rain probability is 12% (Safe: < 30%).
  8. Crop Phenology Agent checks stage: BT Cotton is in "Flowering & Boll Formation" (Peak water sensitivity).
  9. Risk Assessment Agent flags High-Severity Risk: Water Stress (Confidence: 88%).
  10. Master Orchestrator calls LLM Provider with live agronomic context for Gujarati & English explanations.

[Constrained Action Planning]
  11. Action Planner synthesizes Plan #PLAN-1024: Drip Irrigation (2,500 L, ₹45 estimated power cost).
  12. Constraint Engine verifies 4 safety rules:
      - Rain window: 12% < 30% (PASSED)
      - Electricity budget: ₹45 <= ₹150 ceiling (PASSED)
      - Line pressure: 1.8 bar within safe 1.5 - 2.2 bar range (PASSED)
      - Sump water level: Sufficient reserve capacity (PASSED)

[Human-in-the-Loop Approval & Field Actuation]
  13. Plan surfaces on Farmer Dashboard; Kishanbhai clicks "Approve Plan".
  14. ACID Transaction updates plan state to APPROVED and generates dispatched Task #TSK-01.
  15. Execution Agent transmits MQTT command: `{ "action": "OPEN", "duration": 35 }`.
  16. Solenoid Valve SV-01 switches state to RUNNING; front-end badge turns green in real time.

[Absorption Feedback & Verification]
  17. Solenoid runs for scheduled 35 minutes delivering precision irrigation.
  18. Valve switches state to CLOSED upon timer completion.
  19. Task board updates #TSK-01 to COMPLETED.
  20. Post-irrigation sensor reading reflects normalized moisture: 46.2% (Optimal).
  21. Complete trace immutably committed to `activity_logs` and `agent_runs` audit tables.
```

---

## 🤖 The 11 Autonomous Specialized Agents

| # | Agent Name | Domain & Scope | Core Logic & Heuristics | Primary Output |
|---|---|---|---|---|
| **1** | **Master Orchestrator** | Central Nervous System | Coordinates multi-agent graph, resolves conflicting goals, maintains audit trails | Consolidated advisory, consensus state, audit events |
| **2** | **Soil & Moisture** | Hydrology & Subsurface | FDR soil probes, field capacity, wilting point, evapotranspiration rates | Moisture deficit metrics, irrigation requirement scores |
| **3** | **Meteorological** | Agro-Meteorology | Open-Meteo / IMD 7-day forecast, rain probabilities, thermal inversion | Spray safety windows, frost/heat warnings, rain alerts |
| **4** | **Crop Phenology** | Plant Physiology | Growing Degree Days (GDD), BBCH stage index (Flowering, Boll formation) | Stage-specific vulnerability multipliers, critical water windows |
| **5** | **Pest & Pathogen** | Biological Threat Detection | Ambient night humidity, thermal thresholds, regional outbreak alerts | Pink bollworm, aphid & whitefly susceptibility indices |
| **6** | **Disease Diagnostics** | Computer Vision Pathology | Multi-spectral leaf visual analysis, pathogen signature matching | Diagnostic confidence score, organic & chemical remedies |
| **7** | **Nutrient & NPK** | Soil Chemistry | Soil EC, pH, available Nitrogen, Phosphorus, Potassium ratios | Fertigation schedules, deficiency correction plans |
| **8** | **APMC Mandi & Market**| Agricultural Economics | Real-time Agmarknet spot rates, historical trends, MSP margins | Optimal harvest & selling windows, market arbitrage advice |
| **9** | **Risk Assessment** | Multi-Factor Risk Matrix | Deterministic threat prioritization across hydrology, weather, and pests | Prioritized risk severity queue (Critical, High, Medium, Low) |
| **10**| **Constrained Action Planner** | Resource Optimization | Knapsack budget constraints, weather safety windows, water supply checks | Fully qualified executable action plans (`PLAN-XXXX`) |
| **11**| **Execution & Feedback** | Actuation & Verification | MQTT hardware trigger commands, valve state machine, absorption loop | Actuator commands (`OPEN`/`CLOSE`), execution verification logs |

---

## 🌟 Key Platform Capabilities

### 1. 🖥️ Comprehensive Farmer Dashboard
- **Farm Health Score**: Composite agro-metric (0-100) computed from soil moisture, weather stress, and pest pressure.
- **Microclimate Overview**: Instant temperature, humidity, 24-hr rain probability, and sensor battery levels.
- **Active Advisory Spotlight**: Bilingual cards (Gujarati / English) highlighting urgent field interventions.

### 2. 🗺️ Interactive GIS Farm Mapping
- Field polygon boundary mapping for Field A (Cotton), Field B (Groundnut), and Field C (Wheat).
- Real-time stress zone color-coding (Deficit = Amber/Red, Optimal = Emerald, Saturated = Blue).
- Interactive sensor marker popups displaying instant live metrics.

### 3. 🔬 Computer Vision Crop Disease Detector
- Instant photo upload or sample dataset selection.
- Detects cotton leaf curl virus, bacterial blight, cercospora leaf spot, and groundnut rust.
- Recommends **Organic Remedies** (Neem seed kernel extract, sour buttermilk, Dashaparni ark) and **Chemical Interventions** with precise dosages.
- Automatic **Agronomist Escalation** workflow when diagnostic confidence is below 70%.

### 4. 📈 APMC Mandi Market Intelligence
- Real-time market rates across local Gujarat Mandis (Rajkot, Gondal, Amreli, Jasdan).
- MSP (Minimum Support Price) comparison bars and 7-day price trajectory analysis.
- AI-driven "Hold vs. Sell" recommendations based on spot arrivals and price elasticity.

### 5. 🗣️ Kisan Multilingual Voice Assistant
- Voice queries in **Gujarati (ગુજરાતી)**, **Hindi (हिन्दी)**, and **English**.
- **Context-grounded answering**: The voice agent checks actual live farm telemetry (e.g., "Field A moisture is 31.4%") before responding.
- Integrated Web Speech API for zero-latency speech-to-text and text-to-speech feedback.

### 6. 📋 Kanban Field Task Board & Valve Control
- Interactive task management columns: `To Do`, `In Progress`, and `Completed`.
- Real-time manual and automated toggle for Field Solenoid Valves with countdown timers.
- Complete execution audit trail linking every valve open/close to an approved plan.

---

## 📁 Repository Directory Structure

```
local bit n build/
├── .env.example                 # Global environment configuration template
├── start_all.bat                # Windows 1-click launcher for Frontend + Backend
├── krishinetra.db               # SQLite development database (auto-seeded)
├── docs/                        # Architecture & integration specifications
│   └── external-integrations-plan.md  # Detailed external API integration specs
│
├── Backend/                     # FastAPI Backend Platform
│   ├── app/
│   │   ├── main.py              # Application lifespan, CORS, WebSockets, error handlers
│   │   ├── config.py            # Pydantic v2 settings & environment parsing
│   │   ├── database.py          # Async SQLAlchemy engine & session factory
│   │   ├── dependencies.py      # Auth, permission & DB dependency injection
│   │   ├── api/                 # 17 REST API Routers
│   │   │   ├── action_plans.py  # Plan approval, rejection & execution
│   │   │   ├── advisory.py      # AI explainable advisory endpoints
│   │   │   ├── agents.py        # Multi-agent status, runs & orchestration
│   │   │   ├── auth.py          # JWT user authentication
│   │   │   ├── crops.py         # Crop lifecycle & phenology
│   │   │   ├── dashboard.py     # Consolidated farm dashboard summary
│   │   │   ├── disease.py       # Leaf disease CV diagnosis & escalation
│   │   │   ├── farms.py         # Farm & field CRUD operations
│   │   │   ├── market.py        # APMC Mandi price intelligence
│   │   │   ├── monitoring.py    # Live telemetry data aggregation
│   │   │   ├── notifications.py # Multi-channel alerts (Web, SMS)
│   │   │   ├── reports.py       # Weekly & seasonal agro-reports
│   │   │   ├── risks.py         # Detected risk matrix
│   │   │   ├── sensors.py       # Sensor telemetry ingestion & valve triggers
│   │   │   ├── storage.py       # Image upload & signed URLs
│   │   │   ├── tasks.py         # Kanban field task management
│   │   │   ├── voice.py         # Vernacular voice query processing
│   │   │   └── weather.py       # Open-Meteo current & forecast weather
│   │   ├── models/              # SQLAlchemy Declarative ORM models (14+ models)
│   │   ├── schemas/             # Pydantic v2 validation & response DTOs
│   │   ├── services/            # Pure business domain logic
│   │   ├── agents/              # 11 Cooperative Autonomous Agents & Constraint Engine
│   │   ├── integrations/        # MQTT, Weather, Market, LLM, Cloudinary, Redis
│   │   ├── workers/             # Background telemetry jitter & sensor simulator
│   │   └── utils/               # Logger, security & GreenValley farm seeder
│   ├── tests/                   # Pytest automated test suite
│   ├── requirements.txt         # Python backend dependencies
│   ├── Dockerfile               # Backend production container specification
│   └── docker-compose.yml       # Standalone backend + Postgres + Redis compose
│
├── Database/                    # Dedicated Database Architecture & Migration Layer
│   ├── config.py                # Connection pool & failover configuration
│   ├── connection.py            # Sync & async engines and sessionmakers
│   ├── models/                  # 18 Domain Models with comprehensive indexes & relationships
│   ├── repositories/            # Clean Repository Pattern (Base, Farm, Sensor, Plan, etc.)
│   ├── schemas/                 # Pydantic v2 schemas and DTOs
│   ├── migrations/              # Alembic database migration revisions
│   ├── scripts/                 # Schema initializers & demo seeders
│   ├── docker/                  # Docker compose for PostgreSQL 15, Redis 7, Mosquitto MQTT
│   ├── tests/                   # Automated ACID transaction & repository test suite
│   └── requirements.txt         # Database package dependencies
│
└── Frontend/                    # React 18 + Vite Web Application
    ├── index.html               # Application HTML entry point
    ├── vite.config.js           # Vite build configuration
    ├── tailwind.config.js       # Custom agricultural color palette & glassmorphism
    ├── package.json             # NPM dependencies & scripts
    └── src/
        ├── App.jsx              # Main routing, dynamic navbar & sidebar layout
        ├── main.jsx             # React DOM root mounting
        ├── index.css            # Global CSS, Tailwind directives & custom scrollbars
        ├── context/             # Global FarmContext & Multilingual LanguageContext
        ├── data/                # Fallback mock telemetry & translation dictionaries (GU/HI/EN)
        ├── components/          # Reusable UI widgets, layout headers, and maps
        └── pages/               # 15 Complete Page Views
            ├── Dashboard.jsx            # Central farm intelligence overview
            ├── FarmMapPage.jsx          # Interactive Mapbox farm GIS view
            ├── MonitoringPage.jsx       # Sensor fleet telemetry & NPK radar
            ├── RiskDetectionPage.jsx    # Threat detection matrix & evidence
            ├── AIAdvisoryPage.jsx       # Explainable AI recommendations
            ├── ActionPlansPage.jsx      # Constrained multi-factor action plans
            ├── TaskExecutionPage.jsx    # Kanban board & solenoid valve controls
            ├── AgentCenterPage.jsx      # 11-Agent status & live terminal stream
            ├── DiseaseDetectorPage.jsx  # Vision AI crop leaf diagnostics
            ├── WeatherPage.jsx          # Open-Meteo hourly & 7-day agro forecasts
            ├── MarketPage.jsx           # APMC Mandi commodity price charts
            ├── VoiceAssistantPage.jsx   # Multilingual Kisan voice interface
            ├── EscalationPage.jsx       # Agronomist review tickets
            ├── ReportsPage.jsx          # Weekly agricultural summaries & PDF export
            └── FarmSetupPage.jsx        # Farm profile & field polygon editor
```

---

## 🛠️ Technology Stack Matrix

| Layer | Technologies Used | Key Responsibilities |
|---|---|---|
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide React, Recharts, Mapbox GL, Canvas Confetti | Highly responsive, visually rich, multilingual, real-time reactive UI |
| **Backend API** | Python 3.10+, FastAPI, Uvicorn, Pydantic v2 | Async REST API, WebSocket broadcasts, CORS, unified error handling |
| **Multi-Agent System** | LangGraph architectural patterns, Python AsyncIO | Multi-agent coordination, deterministic heuristics, constraint engine |
| **Persistence & ORM** | SQLAlchemy 2.0 Async, Alembic, PostgreSQL 15 / SQLite, Repository Pattern | ACID transactions, automated migrations, relational domain models |
| **Caching & Broker** | Redis 7, Eclipse Mosquitto (Paho MQTT v2) | Low-latency state caching, sensor telemetry pub/sub, valve command topics |
| **External Providers** | Open-Meteo, Google Gemini, Agmarknet, Cloudinary | Real-time weather, LLM synthesis, APMC prices, leaf photo cloud storage |

---

## 🚀 Quick Start Guide

### Option 1: One-Click Startup (Windows)

The simplest way to boot both services simultaneously is using the root launcher script:

```bat
start_all.bat
```
This automatically:
- Launches the **FastAPI Backend** on `http://localhost:8000` (auto-creates tables, seeds data, starts mock IoT).
- Launches the **Vite Frontend** on `http://localhost:5173`.
- Opens your default web browser to the dashboard.

---

### Option 2: Manual Step-by-Step Setup

#### Step 1: Clone & Configure Environment
```bash
git clone <repository-url>
cd "local bit n build"

# Copy environment template
cp .env.example .env
```

#### Step 2: Backend Setup
```bash
# Navigate to Backend
cd Backend

# Create & activate a Python virtual environment (recommended)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI development server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Interactive ReDoc**: `http://localhost:8000/redoc`
- **Live WebSocket**: `ws://localhost:8000/ws/farm/farm-greenvalley-01`

#### Step 3: Frontend Setup
Open a second terminal:
```bash
# Navigate to Frontend
cd Frontend

# Install node dependencies
npm install

# Start Vite development server
npm run dev
```
- **Web Application URL**: `http://localhost:5173`

---

### Option 3: Full Production Docker Deployment

To launch PostgreSQL 15, Redis 7, and the Mosquitto MQTT Broker:

```bash
# Start background infrastructure
cd Database/docker
docker-compose up -d

# Verify all containers are healthy
docker ps
```

In `.env`, update the connection string to PostgreSQL:
```env
DATABASE_URL=postgresql+asyncpg://krishinetra_user:krishinetra_secret_pass@localhost:5432/krishinetra_db
SYNC_DATABASE_URL=postgresql://krishinetra_user:krishinetra_secret_pass@localhost:5432/krishinetra_db
REDIS_URL=redis://localhost:6379/0
USE_MOCK_IOT=false
MQTT_BROKER_HOST=localhost
MQTT_BROKER_PORT=1883
```

Run database migrations:
```bash
alembic -c Database/migrations/alembic.ini upgrade head
```

---

## ⚙️ Environment Variables Reference

| Variable | Default Value | Description |
|---|---|---|
| `APP_NAME` | `"KrishiNetra AI"` | Application title displayed across API docs & logs |
| `APP_ENV` | `development` | Deployment environment (`development` / `production`) |
| `DEBUG` | `true` | Enables verbose SQL logging and reload flags |
| `PORT` | `8000` | Backend listening port |
| `SECRET_KEY` | *(Secret string)* | JWT signature secret key |
| `DATABASE_URL` | `sqlite+aiosqlite:///./krishinetra.db` | Async database connection URL |
| `SYNC_DATABASE_URL` | `sqlite:///./krishinetra.db` | Sync database connection URL (for Alembic migrations) |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis caching connection string |
| `WEATHER_PROVIDER` | `openmeteo` | Weather provider (`openmeteo` [free, no key] or `mock`) |
| `LLM_PROVIDER` | `mock` | LLM synthesis provider (`mock`, `gemini`, or `openai`) |
| `GEMINI_API_KEY` | *(Optional)* | Google Gemini API Key for dynamic vernacular reasoning |
| `MARKET_PROVIDER` | `agmarknet` | APMC Mandi market price provider (`agmarknet` or `mock`) |
| `STORAGE_PROVIDER` | `local` | Upload destination for disease photos (`local`, `cloudinary`, `s3`) |
| `UPLOAD_DIR` | `./uploads` | Local directory for static image uploads |
| `USE_MOCK_IOT` | `true` | Automatically generates realistic sensor jitter & valve simulation |
| `MQTT_BROKER_HOST` | `localhost` | MQTT broker hostname |
| `MQTT_BROKER_PORT` | `1883` | MQTT broker port |

---

## 🧪 Testing & Quality Assurance

KrishiNetra comes with a comprehensive test suite across unit, repository, ACID transaction, and E2E agent pipelines:

### Running Backend Tests
```bash
cd Backend
pytest -v tests/
```

### Running Database Layer & Transaction Tests
```bash
python -m pytest -v Database/tests/
```
*Validates in-memory SQLite fixtures, Base Repository CRUD, ACID atomic plan approvals, and zero-orphan rollbacks.*

### Testing Frontend Production Build
```bash
cd Frontend
npm run build
npm run preview
```

---

## 📡 REST API & WebSocket Specifications

### Primary REST Endpoints

| Category | Method | Endpoint | Description |
|---|---|---|---|
| **Health** | `GET` | `/` | Platform health status and version verification |
| **Dashboard**| `GET` | `/api/dashboard` | Consolidated metrics, soil moisture, and active recommendation |
| **Farms** | `GET` | `/api/farms/{farm_id}` | Farm profile, acreage, and soil characteristics |
| **Fields** | `GET` | `/api/farms/{farm_id}/fields`| Polygon coordinates, crop type, and field status |
| **Sensors** | `GET` | `/api/monitoring/telemetry` | Aggregated sensor readings across moisture, temp, EC, pH |
| **Sensors** | `POST`| `/api/sensors/valve/trigger` | Actuate field solenoid valve (`OPEN` / `CLOSE`) |
| **Risks** | `GET` | `/api/risks` | Prioritized risk items (Water stress, pests, nutrient deficit) |
| **Advisory** | `GET` | `/api/advisory` | Explainable recommendations with transparent decision factors |
| **Plans** | `GET` | `/api/action-plans` | Constrained executable action plans |
| **Plans** | `POST`| `/api/action-plans/{id}/approve`| Farmer approval triggering task dispatch & valve command |
| **Tasks** | `GET` | `/api/tasks` | Field Kanban tasks (`todo`, `in_progress`, `completed`) |
| **Agents** | `GET` | `/api/agents` | Status of all 11 autonomous agents and cycle latency |
| **Agents** | `POST`| `/api/agents/orchestrate` | Force manual full-graph multi-agent deliberation cycle |
| **Disease** | `POST`| `/api/disease/analyze` | Vision AI leaf analysis (multipart file upload or demo ID) |
| **Weather** | `GET` | `/api/weather` | Current weather, hourly metrics, and 7-day spray safety window |
| **Market** | `GET` | `/api/market` | APMC mandi spot prices, MSP margins, and trend analysis |
| **Voice** | `POST`| `/api/voice/query` | Grounded multilingual Q&A in Gujarati, Hindi, and English |

### Real-Time WebSocket Channel
- **Endpoint**: `ws://localhost:8000/ws/farm/{farm_id}`
- **Subscribed Events**:
  - `sensor_update`: Live moisture, temperature, and electrical conductivity changes.
  - `risk_detected`: Instant threat detection alerts.
  - `valve_status`: Field solenoid state transitions (`IDLE` ➡️ `RUNNING` ➡️ `COMPLETED`).
  - `agent_update`: Real-time agent status and audit terminal logs.
  - `task_update`: Task board status sync across multiple field operators.

---

## 🛡️ ACID Safety & Constraint Guarantees

Autonomous execution in agriculture can have costly real-world consequences if left unconstrained. KrishiNetra implements a multi-layer safety framework:

1. **Deterministic Constraint Engine**:
   - Plans are evaluated by rule-based algorithms before being surfaced to the farmer.
   - Plans are automatically blocked if rain probability > 30%, if electrical costs exceed the farmer's budget ceiling, or if valve line pressure is unsafe.
2. **Human-in-the-Loop Governance**:
   - The platform strictly separates **Advisory** from **Actuation**. Critical actions require explicit farmer approval (`approve` endpoint) or authorized automatic policy override.
3. **Atomic Transaction Guarantees**:
   - Approving an action plan, dispatching the physical field task, generating the MQTT actuation payload, and writing to the audit log are wrapped in an atomic database transaction. Any failure results in a full rollback with zero orphaned records.
4. **Fail-Safe Fallbacks**:
   - If the MQTT broker becomes unreachable, the platform automatically engages the `MockIoTDeviceService` with zero frontend disruption.
   - If the external LLM provider experiences latency or downtime, the platform seamlessly falls back to pre-compiled, deterministic agronomic rule templates.

---

## 👥 Contributors & Acknowledgements

- Developed for the **Bit N Build** hackathon / agricultural technology initiative.
- Special thanks to agricultural data providers:
  - [Open-Meteo](https://open-meteo.com/) for high-resolution agro-meteorological data.
  - [Agmarknet / Open Government Data (OGD) India](https://agmarknet.gov.in/) for APMC Mandi rates.
  - Open-source agronomic research on Gujarat agro-climatic zones (Saurashtra region).

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use, modify, and distribute it for precision agriculture research and development.
