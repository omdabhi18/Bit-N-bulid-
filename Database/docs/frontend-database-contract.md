# Frontend-to-Database Mapping Contract

This document provides the definitive contract mapping each existing frontend screen to its API endpoint, backend service, database table, and Pydantic response DTO.

| Frontend Page | UI Component | API Endpoint | Service | Primary Database Table | Response DTO |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dashboard** | `<Dashboard />` | `GET /api/dashboard` | `DashboardService` | `farms`, `fields`, `sensor_readings`, `risks`, `ai_advisories`, `tasks` | `DashboardResponse` |
| **Farm Map & Fields** | `<FarmMapPage />` & `<FarmMapbox />` | `GET /api/farms/fields` | `FarmService` | `fields` | `List[FieldDetail]` |
| **Farm Setup** | `<FarmSetupPage />` | `GET /api/farms/profile` | `FarmService` | `farms`, `crops`, `sensors` | `FarmProfile` |
| **Live Monitoring** | `<MonitoringPage />` | `GET /api/monitoring/telemetry` | `SensorService` | `sensors`, `sensor_readings` | `MonitoringResponse` |
| **IoT Valve Control** | Solenoid Actuator Bar | `POST /api/sensors/valve/trigger` | `SensorService` | `sensors`, `activity_logs` | `ValveTriggerResponse` |
| **Risk Detection** | `<RiskDetectionPage />` | `GET /api/risks` | `RiskService` | `risks` | `List[RiskResponse]` |
| **Plan Generator** | "Generate Action Plan" | `POST /api/risks/{id}/generate-plan` | `RiskService` | `risks`, `action_plans`, `activity_logs` | `{ success, planId }` |
| **AI Advisory** | `<AIAdvisoryPage />` | `GET /api/advisory` | `AdvisoryService` | `ai_advisories` | `List[AdvisoryResponse]` |
| **Advisory Approval** | "Approve Recommendation" | `POST /api/advisory/{id}/approve` | `AdvisoryService` | `ai_advisories`, `activity_logs` | `{ success, message }` |
| **Action Plans** | `<ActionPlansPage />` | `GET /api/action-plans` | `ActionPlanService` | `action_plans` | `List[ActionPlanResponse]` |
| **Plan Approval** | "Approve & Schedule Plan" | `POST /api/action-plans/{id}/approve` | `ActionPlanService` | `action_plans`, `tasks`, `activity_logs` | `{ success, message }` |
| **Task Kanban Board** | `<TaskExecutionPage />` | `GET /api/tasks` | `TaskService` | `tasks` | `List[TaskResponse]` |
| **Task Status Move** | Drag / Status Click | `PATCH /api/tasks/{id}/status` | `TaskService` | `tasks`, `activity_logs` | `TaskResponse` |
| **AI Multi-Agent Center** | `<AgentCenterPage />` | `GET /api/agents` | `Orchestrator` | `agent_runs` | `List[AgentResponse]` |
| **Agent Cycle Run** | "Trigger Cooperative Cycle" | `POST /api/agents/orchestrate` | `Orchestrator` | `agent_runs`, `activity_logs` | `OrchestrateCycleResponse` |
| **Disease Detector** | `<DiseaseDetectorPage />` | `POST /api/disease/analyze` | `DiseaseService` | `disease_analyses` | `DiseaseAnalyzeResponse` |
| **Expert Escalation** | `<EscalationPage />` | `POST /api/disease/escalate` | `DiseaseService` | `expert_requests` | `EscalationResponse` |
| **Weather Forecast** | `<WeatherPage />` | `GET /api/weather` | `WeatherService` | `weather_data` | `WeatherForecastResponse` |
| **Mandi Market Prices** | `<MarketPage />` | `GET /api/market` | `MarketService` | `market_prices` | `List[CommodityResponse]` |
| **Kisan Voice AI** | `<VoiceAssistantPage />` | `POST /api/voice/query` | `VoiceService` | `sensor_readings`, `weather_data`, `market_prices` | `VoiceQueryResponse` |
| **Audit Reports** | `<ReportsPage />` | `GET /api/reports/audit-certificate` | `NotificationService` | `activity_logs`, `farms` | `AuditCertificateResponse` |
