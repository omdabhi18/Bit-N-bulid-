# KrishiNetra AI: Frontend-Backend API Contract Mapping

This document provides the definitive contract specification connecting the existing **KrishiNetra AI – GreenValley Smart Farms** React Frontend (`Frontend/src`) to the FastAPI Modular-Monolith Backend (`Backend/app`).

---

## 1. Dashboard Module (`src/pages/Dashboard.jsx`)

- **Component**: `<Dashboard />`
- **Data Needed**: Overall farm health score, current soil moisture, temperature, weather snippet, crop phenology, overall risk badge, primary critical recommendation, fields overview, pending tasks, live sensor telemetry.
- **Endpoint**: `GET /api/dashboard`
- **Request Schema**: None (Headers: `Authorization: Bearer <token>` optional/default user)
- **Response Schema**: `DashboardResponseSchema`
```json
{
  "farmHealthScore": 82,
  "soilMoisture": 31.4,
  "soilMoistureStatus": "Deficit (પાણીની જરૂર)",
  "soilTemperature": 27.8,
  "airTemperature": 33.2,
  "airHumidity": 58,
  "rainfallProb24h": 12,
  "overallRisk": "High",
  "activeRisksCount": 3,
  "primaryAdvisory": {
    "id": "adv-01",
    "title": "Urgent Drip Irrigation for Cotton Field A",
    "titleGu": "કપાસ પ્લોટ A માં તાત્કાલિક ડ્રિપ પિયત આપવું",
    "titleHi": "कपास खेत A में तुरंत ड्रिप सिंचाई करें",
    "field": "Field A (Cotton)",
    "priority": "High",
    "confidenceScore": 91,
    "status": "Pending Approval",
    "timestamp": "10:15 AM Today",
    "orchestratorSummary": "Water stress detected in flowering crop stage. AI recommends executing irrigation today between 6:00 PM and 8:00 PM."
  },
  "fields": [...],
  "pendingTasks": [...],
  "activeValve": { "fieldA": false, "fieldB": false, "fieldC": false }
}
```
- **Database Model**: `Farm`, `Field`, `SensorReading`, `Risk`, `AIAdvisory`, `FarmTask`
- **Service**: `DashboardService.get_dashboard_summary()`
- **Agent/Integration**: `MasterOrchestrator`, `SoilAgent`, `WeatherAgent`

---

## 2. Farm Map & Fields (`src/pages/FarmMapPage.jsx`)

- **Component**: `<FarmMapPage />` & `<FarmMapbox />`
- **Data Needed**: Farm profile, polygon coordinates of Field A, B, and C, crop type, acreage, soil PH, NPK status, drip readiness, real-time stress zone coloring.
- **Endpoint**: `GET /api/farms/{farm_id}/fields`
- **Response Schema**: `List[FieldDetailSchema]`
- **Field CRUD**:
  - `GET /api/fields/{field_id}`
  - `POST /api/fields`
  - `PATCH /api/fields/{field_id}`
- **Database Model**: `Farm`, `Field`, `Crop`, `SensorNode`
- **Service**: `FarmService`

---

## 3. Live Sensors & Telemetry (`src/pages/MonitoringPage.jsx`)

- **Component**: `<MonitoringPage />`
- **Data Needed**: Realtime telemetry (moisture, temp, EC, pH, NPK), 24-hour time series, NPK radar charts, hardware sensor fleet status (battery, signal, sync time).
- **Endpoints**:
  - `GET /api/monitoring/telemetry`
  - `GET /api/sensors/fleet`
  - `POST /api/sensors/ingest` (Ingests telemetry from edge IoT node or simulator)
  - `POST /api/sensors/valve/trigger` (Opens/closes field solenoid valve)
- **Database Model**: `SensorNode`, `SensorReading`
- **Service**: `SensorService`, `MockIoTDeviceService`
- **Agent/Integration**: `MQTTClient` on topic `farm/{id}/field/{id}/sensor` & `valve`

---

## 4. Risk Detection Matrix (`src/pages/RiskDetectionPage.jsx`)

- **Component**: `<RiskDetectionPage />`
- **Data Needed**: 6 categories of detected risks (Water stress, Pest risk, Nutrient deficiency, Weather risk, Market timing risk), evidence indicators, probability score, action plan link.
- **Endpoints**:
  - `GET /api/risks`
  - `POST /api/risks/{risk_id}/generate-plan`
- **Response Schema**: `List[RiskResponseSchema]`
- **Database Model**: `Risk`, `ActionPlan`
- **Service**: `RiskService`, `ActionPlanService`
- **Agent/Integration**: `RiskAgent`, `SoilAgent`, `PestAgent`, `ConstrainedActionPlanner`

---

## 5. AI Advisory & Explainability (`src/pages/AIAdvisoryPage.jsx`)

- **Component**: `<AIAdvisoryPage />`
- **Data Needed**: Transparent AI recommendations with zero black-box factor breakdown (Moisture deficit, Rain prob, Soil temp, Crop stage) and narrative "Why" reasoning.
- **Endpoints**:
  - `GET /api/advisory`
  - `POST /api/advisory/{id}/approve`
  - `POST /api/advisory/{id}/reject`
- **Response Schema**: `List[AdvisoryResponseSchema]`
- **Database Model**: `AIAdvisory`, `ExplainabilityFactor`, `ActivityLog`
- **Service**: `AdvisoryService`
- **Agent/Integration**: `MasterOrchestrator`, `LLMProvider` (Gemini / OpenAI / Mock)

---

## 6. Constrained Action Plans (`src/pages/ActionPlansPage.jsx`)

- **Component**: `<ActionPlansPage />`
- **Data Needed**: Multi-factor constrained plans verified against budget ceilings, weather safety windows, water supplies, and protective protocols.
- **Endpoints**:
  - `GET /api/action-plans`
  - `POST /api/action-plans/{id}/approve`
  - `POST /api/action-plans/{id}/execute`
- **Plan States**: `DRAFT`, `PENDING_APPROVAL`, `APPROVED`, `SCHEDULED`, `EXECUTING`, `COMPLETED`, `FAILED`, `CANCELLED`
- **Database Model**: `ActionPlan`, `PlanConstraint`
- **Service**: `ActionPlanService`, `ConstraintEngine`
- **Agent/Integration**: `ConstrainedActionPlanner`, `ExecutionAgent`

---

## 7. Task Execution Kanban (`src/pages/TaskExecutionPage.jsx`)

- **Component**: `<TaskExecutionPage />`
- **Data Needed**: Field tasks organized by `todo`, `in-progress`, `completed`. Solenoid valve status bar and task creation modal.
- **Endpoints**:
  - `GET /api/tasks`
  - `POST /api/tasks`
  - `PATCH /api/tasks/{id}/status`
- **Database Model**: `FarmTask`, `ActivityLog`
- **Service**: `TaskService`
- **Agent/Integration**: `ExecutionAgent`

---

## 8. AI Multi-Agent Center (`src/pages/AgentCenterPage.jsx`)

- **Component**: `<AgentCenterPage />`
- **Data Needed**: Real-time status of 8-11 specialized autonomous agents, confidence ratings, last cycle runtime, inputs, outputs, current tasks, and live audit terminal stream.
- **Endpoints**:
  - `GET /api/agents`
  - `POST /api/agents/orchestrate` (Manually triggers a full multi-agent synthesis cycle)
  - `GET /api/agents/audit-logs`
- **Database Model**: `AgentRun`, `ActivityLog`
- **Service**: `OrchestratorService`
- **Agent/Integration**: `LangGraph / StateGraph Orchestrator`

---

## 9. Crop Disease Vision AI (`src/pages/DiseaseDetectorPage.jsx`)

- **Component**: `<DiseaseDetectorPage />`
- **Data Needed**: Uploaded or sample leaf image diagnosis, confidence score, pathogen signature, organic remedies (e.g. Neem seed extract, Gomutra), chemical cures, and agronomist escalation ticket.
- **Endpoints**:
  - `POST /api/disease/analyze` (Multipart file upload or sample payload)
  - `POST /api/disease/escalate` (Agronomist escalation if confidence < 70%)
- **Database Model**: `DiseaseAnalysis`, `ExpertReviewTicket`
- **Service**: `DiseaseService`
- **Agent/Integration**: `DiseaseAgent`, `StorageProvider`

---

## 10. Weather Intelligence (`src/pages/WeatherPage.jsx`)

- **Component**: `<WeatherPage />`
- **Data Needed**: Current weather, hourly forecast, 7-day forecast, ET0 evapotranspiration rate, agricultural spray safety windows.
- **Endpoint**: `GET /api/weather`
- **Database Model**: `WeatherRecord`
- **Service**: `WeatherService`
- **Agent/Integration**: `WeatherProvider` (IMD / OpenWeather / Mock)

---

## 11. Mandi Market Prices (`src/pages/MarketPage.jsx`)

- **Component**: `<MarketPage />`
- **Data Needed**: Cotton, Wheat, Groundnut prices, 7-day trend, MSP comparison, nearby mandis (Rajkot, Gondal, Amreli), AI optimal selling window advice.
- **Endpoint**: `GET /api/market`
- **Database Model**: `MarketCommodity`, `MandiPrice`
- **Service**: `MarketService`
- **Agent/Integration**: `MarketProvider` (Agmarknet / Mock)

---

## 12. Kisan Multilingual Voice AI (`src/pages/VoiceAssistantPage.jsx`)

- **Component**: `<VoiceAssistantPage />`
- **Data Needed**: Question answering in Gujarati (`GU`), Hindi (`HI`), and English (`EN`) that retrieves live farm telemetry (Field A moisture, rain prob, crop stage, prices) before replying.
- **Endpoint**: `POST /api/voice/query`
- **Request Schema**: `{ "query": "Mara khedut ma aaje pani aapvu joie?", "language": "gu" }`
- **Response Schema**: `{ "replyText": "...", "actionRecommendation": "irrigate", "language": "gu" }`
- **Service**: `VoiceService`
- **Agent/Integration**: `LLMProvider`, `FarmContextRetrieval`

---

## 13. Real-Time WebSocket (`/ws/farm/{farm_id}`)

- **Protocol**: WebSocket
- **Broadcast Events**:
  - `sensor_update`: `{ "soilMoisture": 31.4, "temp": 27.8, "ec": 0.42 }`
  - `risk_detected`: `{ "riskId": "risk-01", "category": "Water Stress" }`
  - `agent_update`: `{ "agent": "Soil Agent", "status": "Active" }`
  - `action_plan_created`: `{ "planId": "PLAN-1024" }`
  - `task_update`: `{ "taskId": "TSK-01", "status": "completed" }`
  - `valve_status`: `{ "fieldId": "field-a", "status": "Running" }`
  - `alert_created`: `{ "title": "Critical Water Deficit", "severity": "warning" }`
