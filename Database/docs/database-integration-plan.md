# Database Integration & Audit Plan

**Project:** KrishiNetra AI — Autonomous Farm-to-Field Advisory & Action Orchestration Platform  
**Target Database:** PostgreSQL 15+ (Production) / SQLAlchemy Async ORM + SQLite (Local Dev Fallback)

---

## 1. Existing Frontend Architecture
- **Framework**: React 18 with Vite, React Router v6, Tailwind CSS, Recharts, Lucide React, Mapbox GL.
- **Pages**:
  1. `Dashboard.jsx`: Overall farm score, moisture, temperature, active risks, primary advisory, fields preview, pending tasks.
  2. `FarmMapPage.jsx`: Interactive vector/canvas digital twin, field polygons (Field A, B, C), zone health markers.
  3. `MonitoringPage.jsx`: 24h telemetry trends, NPK radar charts, hardware sensor fleet status.
  4. `RiskDetectionPage.jsx`: 6 risk categories, indicators, probability, plan generation buttons.
  5. `AIAdvisoryPage.jsx`: Explainability factor matrix, whyText narrative, approve/dismiss actions.
  6. `ActionPlansPage.jsx`: Budget, weather, safety constraints, plan approval.
  7. `TaskExecutionPage.jsx`: Kanban task board (todo, in-progress, completed), solenoid valve actuators.
  8. `AgentCenterPage.jsx`: 11 specialized autonomous agents status, confidence, runtime, inputs/outputs.
  9. `DiseaseDetectorPage.jsx`: Vision leaf diagnostic scanner, pathogen signature, organic remedies.
  10. `WeatherPage.jsx`: Current weather, hourly forecast, 7-day spray suitability rating.
  11. `MarketPage.jsx`: APMC mandi spot prices (Rajkot, Gondal, Amreli), 7-day trends, MSP comparison.
  12. `VoiceAssistantPage.jsx`: Kisan voice assistant with contextual farm answering in Gujarati, Hindi, English.
  13. `FarmSetupPage.jsx`: Farm acreage, soil characteristics, crop varieties, sensor fleet configuration.
  14. `ReportsPage.jsx`: Verifiable printable health audit certificate.
  15. `EscalationPage.jsx`: University agronomist expert review escalation tickets.

---

## 2. Existing Backend Architecture
- **Framework**: Python 3.10+ with FastAPI.
- **Organization**: Modular monolith in `Backend/app/` with API layer, service layer, multi-agent layer, integration layer, and models.
- **Communication Protocol**: RESTful JSON APIs and bi-directional WebSockets (`/ws/farm/{farm_id}`).
- **Authentication**: JWT Bearer tokens with Argon2/Bcrypt password hashing and RBAC (`FARMER`, `EXPERT`, `ADMIN`).

---

## 3. Existing API Endpoints
- `GET /api/dashboard`
- `GET /api/farms/profile`, `GET /api/farms/fields`
- `GET /api/crops`
- `GET /api/monitoring/telemetry`
- `POST /api/sensors/valve/trigger`, `POST /api/sensors/valve/stop`
- `GET /api/risks`, `POST /api/risks/{id}/generate-plan`
- `GET /api/advisory`, `POST /api/advisory/{id}/approve`, `POST /api/advisory/{id}/reject`
- `GET /api/action-plans`, `POST /api/action-plans/{id}/approve`
- `GET /api/tasks`, `POST /api/tasks`, `PATCH /api/tasks/{id}/status`
- `GET /api/agents`, `POST /api/agents/orchestrate`
- `GET /api/disease/catalog`, `POST /api/disease/analyze`, `POST /api/disease/escalate`, `GET /api/disease/escalations`
- `GET /api/weather`
- `GET /api/market`
- `POST /api/voice/query`
- `GET /api/notifications/activity-logs`
- `GET /api/reports/audit-certificate`

---

## 4. Required Database Schema (The 18 Relational Models)
1. `users`: User identity, password hash, role (`FARMER`, `EXPERT`, `ADMIN`), timestamps.
2. `farms`: Farm property records, coordinates, acreage, soil classification.
3. `fields`: Field boundary polygons, health scores, current moisture, drip status.
4. `crops`: Crop varieties, phenological stage, planting and expected harvest dates.
5. `sensors`: Hardware nodes, device UUID, telemetry capability, battery, signal.
6. `sensor_readings`: Time-series sensor logs with composite index on `(sensor_id, recorded_at)`.
7. `weather_data`: Microclimate weather forecasts, ET0 evapotranspiration rates.
8. `market_prices`: APMC mandi spot prices, price history, arrival volumes.
9. `risks`: Evaluated farm risks with probability, severity, and evidence indicators.
10. `ai_advisories`: Transparent AI recommendations with explainability factors and whyText.
11. `action_plans`: Execution action plans constrained by budget, weather windows, and safety rules.
12. `tasks`: Kanban field execution tasks linked to action plans and assignees.
13. `disease_analyses`: Leaf image vision diagnosis, confidence score, organic and chemical remedies.
14. `expert_requests`: Agronomist review tickets for cases where AI confidence < 70%.
15. `agent_runs`: Execution logs, duration, inputs, outputs for all 11 autonomous agents.
16. `alerts`: Immediate push/in-app alert notifications.
17. `notifications`: Multi-channel notification delivery (Web, SMS, WhatsApp).
18. `activity_logs`: Immutable chronological audit trail demonstrating autonomous system actions.

---

## 5. Migration & Rollback Strategy
- **Tool**: Alembic.
- **Command**: `alembic upgrade head` creates all 18 tables, indexes, and constraints.
- **Rollback**: `alembic downgrade -1` safely rolls back the latest migration revision.
- **Pure SQL Alternative**: `Database/scripts/schema.sql` can be executed directly into any fresh PostgreSQL instance (`psql -d krishinetra_db -f schema.sql`).

---

## 6. Risks & Mitigation
| Risk | Potential Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| Database connection failure | Backend crashes | Implement connection retry with exponential backoff and SQLite fallback |
| Partial action plan execution | Database in inconsistent state | Wrap action plan approval + task creation in ACID database transactions |
| High sensor reading volume | Query latency in telemetry | Add composite index on `(sensor_id, recorded_at)` and enforce pagination |
| Breaking existing Frontend | UI elements fail to render | Keep API schemas decoupled from raw DB models using Pydantic DTOs |
