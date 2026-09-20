# 🔌 External Integrations Plan & Architecture Audit

**Project**: Autonomous Farm-to-Field Advisory & Action Orchestration Platform (KrishiNetra AI)  
**Location**: GreenValley Smart Farms, Rajkot, Gujarat  
**Target Services**: Weather API, LLM API, MQTT / IoT, Indian Mandi Price API, Cloudinary / S3 Storage, Vernacular Voice AI  

---

## 🏛️ End-to-End Architectural Flow

```
Existing Frontend (React + Tailwind + Lucide + Vite)
                         ↓
Existing Backend API Router (`/api/*`)
                         ↓
Service Layer (`app/services/*`)
                         ↓
Integration Layer / Provider Abstractions (`app/integrations/*`)
                         ↓
External APIs / IoT Gateways (Open-Meteo, Gemini/OpenAI, Paho MQTT, Agmarknet, Cloudinary, Redis)
                         ↓
Database & Agent Runs (`krishinetra.db` / PostgreSQL + Redis Cache)
                         ↓
Autonomous AI Agents (11 Agents logging to `agent_runs`)
                         ↓
WebSocket Broadcast (`/ws/farm/{farm_id}`)
                         ↓
Reactive Frontend Updates
```

---

## 📑 Detailed Integration Matrix

| Integration | Provider / Protocol | Backend Module | API Endpoints | Database Tables | Frontend Page | Environment Variables | Failure Fallback | Testing Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Weather API** | `OpenMeteoWeatherProvider` (REST API, no key required) / `MockWeatherProvider` | `app/integrations/weather_provider.py`<br>`app/services/weather_service.py` | `GET /api/weather/current`<br>`GET /api/weather/forecast`<br>`GET /api/weather/hourly`<br>`GET /api/weather/window` | `weather_data`, `weather_records`, `farms` (for coordinates) | `WeatherPage.jsx`<br>`Dashboard.jsx` | `WEATHER_PROVIDER`<br>`WEATHER_API_KEY` | Serve Redis cache; if Redis unavailable, serve latest DB record; fallback to local agro-met station default | Unit tests with mock responses; live Open-Meteo integration test for Rajkot (21.9619, 70.7923) |
| **2. LLM API** | `GeminiLLMProvider` (`google-genai`) / `OpenAILLMProvider` / `MockLLMProvider` | `app/integrations/llm_client.py`<br>`app/agents/orchestrator.py` | Internal Agent Calls<br>`POST /api/agents/orchestrate`<br>`POST /api/voice/query` | `agent_runs`<br>`ai_advisories` | `AIAdvisoryPage.jsx`<br>`AgentCenterPage.jsx`<br>`VoiceAssistantPage.jsx` | `LLM_PROVIDER`<br>`LLM_API_KEY`<br>`GEMINI_API_KEY`<br>`OPENAI_API_KEY` | Timeout after 10s; 2 retries; fallback to deterministic agronomic rule templates without crashing | Test prompt construction, timeout handling, retry backoff, Gujarati/Hindi output, and `agent_runs` DB logging |
| **3. MQTT / IoT** | `PahoMQTTProvider` (Paho MQTT v2 Client) / `MockIoTDeviceService` | `app/integrations/mqtt_client.py`<br>`app/services/iot_service.py`<br>`app/workers/sensor_worker.py` | `POST /api/sensors/valve/trigger`<br>`POST /api/sensors/valve/stop`<br>`GET /api/monitoring/telemetry` | `sensors`, `sensor_nodes`, `sensor_readings`, `tasks`, `activity_logs` | `MonitoringPage.jsx`<br>`TaskExecutionPage.jsx`<br>`Dashboard.jsx` | `MQTT_BROKER_HOST`<br>`MQTT_BROKER_PORT`<br>`MQTT_USERNAME`<br>`MQTT_PASSWORD`<br>`USE_MOCK_IOT` | If MQTT broker is unreachable, activate `MockIoTDeviceService` automatically with identical interface | Validate JSON payloads, reject out-of-range values, verify valve state machine (OPEN -> RUNNING -> CLOSED -> COMPLETED) |
| **4. Mandi Price API** | `AgmarknetOGDProvider` (Agmarknet / Open Government Data) / `MockMarketProvider` | `app/integrations/market_provider.py`<br>`app/services/market_service.py` | `GET /api/market/prices`<br>`GET /api/market/history`<br>`GET /api/market/nearby`<br>`GET /api/market/trends` | `market_prices`, `market_commodities` | `MarketPage.jsx` | `MARKET_PROVIDER`<br>`MARKET_API_KEY` | Return latest cached Mandi rates from Redis/PostgreSQL; if completely offline, display "Market data temporarily unavailable" | Test price parser for Rajkot/Gondal mandis, historical trend calculations, and unavailable state rendering |
| **5. Cloudinary / S3 Storage** | `CloudinaryStorageProvider` / `S3StorageProvider` / `LocalStorageProvider` | `app/integrations/storage_provider.py`<br>`app/services/disease_service.py` | `POST /api/disease/analyze` (multipart file upload) | `disease_analyses` (`image_url`, `crop_id`, `pest`) | `DiseaseDetectorPage.jsx` | `STORAGE_PROVIDER`<br>`CLOUDINARY_CLOUD_NAME`<br>`CLOUDINARY_API_KEY`<br>`CLOUDINARY_API_SECRET`<br>`AWS_BUCKET_NAME` | If Cloudinary upload fails, fallback to `./uploads/` local storage; log error; prevent upload failure from crashing AI analysis | Test file type validation (PNG/JPG/WEBP), 10MB size limit, signed URL generation, and fallback |
| **6. Vernacular Voice AI** | `SpeechToTextProvider` & `TextToSpeechProvider` (Whisper, Google Cloud TTS, Web Speech fallback) | `app/integrations/speech_to_text.py`<br>`app/integrations/text_to_speech.py`<br>`app/services/voice_service.py` | `POST /api/voice/query`<br>`POST /api/voice/transcribe` | `activity_logs`, `sensor_readings`, `fields` | `VoiceAssistantPage.jsx`<br>`VoiceSpeaker.jsx` | `VOICE_STT_PROVIDER`<br>`VOICE_TTS_PROVIDER`<br>`VOICE_TTS_API_KEY` | If STT fails, accept raw text input; if TTS fails, return text reply with client-side SpeechSynthesis metadata | Test Gujarati/Hindi voice query resolution, live telemetry grounding (moisture 31.4%), and audio synthesis fallback |

---

## 🏷️ Centralized MQTT Topic Hierarchy

All MQTT topics are generated through a centralized topic builder (`app/integrations/mqtt_client.py`):

```python
def build_telemetry_topic(farm_id: str, field_id: str, sensor_id: str) -> str:
    return f"farm/{farm_id}/field/{field_id}/sensor/{sensor_id}/telemetry"

def build_status_topic(farm_id: str, field_id: str, device_id: str) -> str:
    return f"farm/{farm_id}/field/{field_id}/device/{device_id}/status"

def build_command_topic(farm_id: str, field_id: str, device_id: str) -> str:
    return f"farm/{farm_id}/field/{field_id}/device/{device_id}/command"
```

---

## ⚡ Autonomous 21-Step Execution Verification Flow

1. **IoT Sensor** publishes `{ "device_id": "SN-Cotton-01", "soil_moisture": 31.4, "temperature": 27.8 }` to MQTT topic.
2. **MQTT Client** receives message and passes to `sensor_worker`.
3. **Sensor Worker** validates numeric constraints (moisture between 0 and 100).
4. **PostgreSQL / SQLite** records reading in `sensor_readings` table.
5. **WebSocket** (`/ws/farm/farm-greenvalley-01`) broadcasts `sensor_update` to connected frontend clients.
6. **Soil Agent** evaluates root-zone threshold (`31.4% < 35%` critical deficit).
7. **Weather Agent** queries `WeatherProvider.get_rain_probability()` -> 12% rain probability.
8. **Crop Agent** verifies BT Cotton is in *Flowering & Boll Formation* stage (peak yield impact).
9. **Risk Agent** calculates `Risk #1: Water Stress (High Severity, 88% probability)`.
10. **LLM Provider** generates farmer explainability summary in Gujarati & English.
11. **Action Planner** synthesizes Plan `PLAN-1024` (Drip Irrigation, 2,500 L, ₹45 estimated electricity cost).
12. **Constraint Engine** validates:
    - Weather window: Rain prob 12% < 30% (Safe)
    - Budget: ₹45 < ₹150 Max (Safe)
    - Safety: Valve line pressure 1.8 bar (Safe)
13. **Farmer** approves advisory / plan on frontend.
14. **Execution Agent** sends command `{ "action": "OPEN", "duration": 35 }` to `farm/.../valve/command`.
15. **MQTT / Mock IoT Valve** transitions state to `RUNNING`.
16. **Frontend** reflects active valve indicator without page refresh.
17. **Execution Timer** completes 35-minute irrigation run.
18. **Valve** transitions state to `CLOSED`.
19. **Task Board** updates `TSK-01` to `COMPLETED`.
20. **Subsequent Sensor Reading** reflects normalized moisture (`46.2% - Optimal`).
21. **Activity Log** immutably commits each step with timestamps and agent signatures.
