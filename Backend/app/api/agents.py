from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.agents.orchestrator import orchestrator
from app.schemas.agent import AgentResponse, OrchestrateCycleRequest, OrchestrateCycleResponse

router = APIRouter(prefix="/agents", tags=["AI Multi-Agent Center"])

STATIC_AGENTS = [
    {
        "id": "orchestrator",
        "name": "Master Orchestrator Agent",
        "role": "System Coordinator & Decision Synthesizer",
        "status": "Active",
        "confidence": 96,
        "lastRun": "1 min ago",
        "currentTask": "Synthesizing soil deficit & weather forecast into action schedule",
        "inputs": ["Soil Agent telemetry", "Weather API 7-day", "Crop phenology state"],
        "outputs": ["Plan #1024 Generated", "Advisory #01 Released", "Risk Matrix Updated"],
        "icon": "Brain"
    },
    {
        "id": "soil",
        "name": "Soil & Moisture Agent",
        "role": "Root Zone Telemetry & Nutrient Modeler",
        "status": "Active",
        "confidence": 94,
        "lastRun": "3 mins ago",
        "currentTask": "Continuously calculating soil water depletion in Field A root zone",
        "inputs": ["FDR moisture probes", "Soil temp 27.8°C", "pH 6.8", "EC 0.42"],
        "outputs": ["Water Deficit Alert (31.4%)", "Phosphorus Low Flag (14 mg/kg)"],
        "icon": "Layers"
    },
    {
        "id": "weather",
        "name": "Meteorological Agent",
        "role": "Hyperlocal Weather & Microclimate Forecast",
        "status": "Active",
        "confidence": 92,
        "lastRun": "4 mins ago",
        "currentTask": "Scanning Doppler radar and IMD satellite layers for rain chances",
        "inputs": ["IMD regional grid", "Local barometric pressure", "Wind velocity 14 km/h"],
        "outputs": ["Rainfall 24h: 12%", "Safe Spray Window: Tomorrow 07:00-10:00"],
        "icon": "CloudSun"
    },
    {
        "id": "crop",
        "name": "Crop Phenology & Health Agent",
        "role": "Growth Stage & Yield Optimization",
        "status": "Active",
        "confidence": 89,
        "lastRun": "7 mins ago",
        "currentTask": "Estimating cotton flowering water sensitivity index",
        "inputs": ["Sowing date June 15", "GDD (Growing Degree Days): 1120", "NDVI 0.72"],
        "outputs": ["Flowering stage confirmed", "Critical water stress vulnerability = High"],
        "icon": "Sprout"
    },
    {
        "id": "pest",
        "name": "Pest & Pathogen Vision Agent",
        "role": "Early Disease Warning & Bio-controls",
        "status": "Active",
        "confidence": 88,
        "lastRun": "12 mins ago",
        "currentTask": "Matching leaf chlorosis image patterns with regional pest outbreak",
        "inputs": ["Thermal imaging", "Field B photo scans", "Nighttime humidity > 78%"],
        "outputs": ["Aphid Risk = 78%", "Recommended Neem 1500ppm bio-spray"],
        "icon": "Bug"
    },
    {
        "id": "market",
        "name": "APMC Mandi & Market Agent",
        "role": "Price Arbitrage & Optimal Harvest Timing",
        "status": "Active",
        "confidence": 90,
        "lastRun": "15 mins ago",
        "currentTask": "Evaluating spot prices across Rajkot, Gondal, and Amreli mandis",
        "inputs": ["Agmarknet API", "Commodity futures", "Local arrival volumes"],
        "outputs": ["Cotton Rate ₹7,380 (+4.2%)", "Suggested Selling Window: 4-6 Days"],
        "icon": "TrendingUp"
    },
    {
        "id": "planner",
        "name": "Constrained Action Planner",
        "role": "Constraint Solver (Cost, Weather, Resources)",
        "status": "Active",
        "confidence": 93,
        "lastRun": "1 min ago",
        "currentTask": "Validating irrigation run time against electricity tariff & rain window",
        "inputs": ["Advisory #01", "Max budget constraint ₹150", "Weather safe window"],
        "outputs": ["Plan #1024 parameters locked (35 mins, ₹45, 18:00 IST)"],
        "icon": "CalendarCheck"
    },
    {
        "id": "execution",
        "name": "Execution & Feedback Agent",
        "role": "IoT Valve Triggers, Notifications & Escalation",
        "status": "Active",
        "confidence": 98,
        "lastRun": "Just now",
        "currentTask": "Monitoring farmer SMS/WhatsApp acknowledgment and valve heartbeat",
        "inputs": ["Plan #1024 Approved status", "SV-01 valve ping", "SMS gateway"],
        "outputs": ["Valve SV-01 armed for 18:00", "Push notification sent to farmer"],
        "icon": "Cpu"
    }
]

@router.get("", response_model=List[AgentResponse])
async def get_agents():
    return [AgentResponse(**a) for a in STATIC_AGENTS]

@router.post("/orchestrate", response_model=OrchestrateCycleResponse)
async def trigger_orchestration_cycle(req: OrchestrateCycleRequest = None):
    farm_id = req.farmId if req else "farm-greenvalley-01"
    state = await orchestrator.process_farm_event(farm_id=farm_id)
    return OrchestrateCycleResponse(
        success=True,
        cycleId=state["agent_executions"][0]["details"].get("cycleId", "cycle-101"),
        executionTimeMs=state["agent_executions"][0]["duration_ms"],
        agentsRan=[a["name"] for a in state["agent_executions"]],
        detectedRisksCount=len(state["detected_risks"]),
        generatedPlansCount=len(state["generated_plans"]),
        summary=f"Cooperative cycle completed with {len(state['detected_risks'])} active risks and {len(state['generated_plans'])} plans"
    )

@router.get("/runs")
async def get_agent_runs(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Retrieve execution log of autonomous agents from agent_runs table."""
    from sqlalchemy.future import select
    from app.models.agent import AgentRun
    res = await db.execute(select(AgentRun).order_by(AgentRun.started_at.desc()).limit(limit))
    rows = res.scalars().all()
    return [
        {
            "id": r.id,
            "agent_name": r.agent_name,
            "field_id": r.field_id,
            "role": r.role,
            "status": r.status,
            "confidence": r.confidence,
            "input_summary": r.input_summary,
            "output_summary": r.output_summary,
            "execution_time_ms": r.execution_time_ms,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "error_message": r.error_message
        }
        for r in rows
    ]
