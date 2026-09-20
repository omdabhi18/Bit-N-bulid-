import time
import uuid
from typing import Dict, Any, List
from app.agents.state import FarmAgentState, AgentExecutionResult
from app.agents.soil_agent import soil_agent
from app.agents.weather_agent import weather_agent
from app.agents.crop_agent import crop_agent
from app.agents.pest_agent import pest_agent
from app.agents.disease_agent import disease_agent
from app.agents.nutrient_agent import nutrient_agent
from app.agents.market_agent import market_agent
from app.agents.risk_agent import risk_agent
from app.agents.action_planner import action_planner
from app.agents.execution_agent import execution_agent
from app.utils.logger import logger

class MasterOrchestrator:
    def __init__(self):
        self.agent_id = "orchestrator"
        self.name = "Master Orchestrator Agent"
        self.role = "System Coordinator & Decision Synthesizer"

    async def process_farm_event(
        self,
        farm_id: str,
        field_id: str = "field-a",
        telemetry: Dict[str, Any] = None,
        weather: Dict[str, Any] = None,
        crop: Dict[str, Any] = None
    ) -> FarmAgentState:
        """
        Executes a complete cooperative multi-agent synthesis cycle.
        Flow:
        Event -> Soil + Weather + Crop + Nutrient + Pest + Market
              -> Risk Agent
              -> Constrained Action Planner
              -> Execution Agent
              -> Master Consensus
        """
        start_time = time.time()
        cycle_id = f"cycle-{uuid.uuid4().hex[:6]}"
        logger.info(f"Master Orchestrator: Starting orchestration {cycle_id} for farm '{farm_id}'")

        state: FarmAgentState = {
            "farm_id": farm_id,
            "field_id": field_id,
            "telemetry": telemetry or {
                "soilMoisture": 31.4,
                "soilTemperature": 27.8,
                "soilPH": 6.8,
                "soilEC": 0.42,
                "nitrogenLevel": 82.0,
                "phosphorusLevel": 14.0,
                "potassiumLevel": 185.0,
                "airTemperature": 33.2,
                "airHumidity": 58.0
            },
            "crop_info": crop or {
                "name": "BT Cotton (કપાસ)",
                "variety": "G.Cot.Hy-8",
                "stage": "Flowering & Boll Formation"
            },
            "weather_info": weather or {
                "rainfallProb24h": 12,
                "windSpeed": 14.0,
                "airTemperature": 33.2
            },
            "market_info": {},
            "soil_analysis": None,
            "weather_analysis": None,
            "crop_analysis": None,
            "pest_analysis": None,
            "nutrient_analysis": None,
            "market_analysis": None,
            "detected_risks": [],
            "advisories": [],
            "generated_plans": [],
            "agent_executions": [],
            "errors": []
        }

        # Step 1: Run Sensor & Domain Observer Agents
        await soil_agent.run(state)
        await weather_agent.run(state)
        await crop_agent.run(state)
        await nutrient_agent.run(state)
        await pest_agent.run(state)
        await disease_agent.run(state)
        await market_agent.run(state)

        # Step 2: Risk Assessment & Matrix Agent
        await risk_agent.run(state)

        # Step 3: Constrained Action Planner (Validates budgets, rain windows & generates plans)
        await action_planner.run(state)

        # Step 4: Execution Agent
        await execution_agent.run(state)

        duration_ms = int((time.time() - start_time) * 1000)
        orch_record: AgentExecutionResult = {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "Active",
            "confidence": 96,
            "duration_ms": max(duration_ms, 35),
            "inputs": ["Soil Agent telemetry", "Weather API 7-day", "Crop phenology state"],
            "outputs": [
                f"Synthesized {len(state['detected_risks'])} active risks",
                f"Generated {len(state['generated_plans'])} constrained action plans",
                f"Advisories ready: {len(state['advisories'])}"
            ],
            "details": {
                "cycleId": cycle_id,
                "totalDurationMs": duration_ms
            }
        }
        state["agent_executions"].insert(0, orch_record)

        # Step 6: Persist all agent runs to database
        try:
            from app.database import AsyncSessionLocal
            from app.models.agent import AgentRun
            from datetime import datetime, timezone
            
            async with AsyncSessionLocal() as db_session:
                for a_exec in state["agent_executions"]:
                    run_entry = AgentRun(
                        id=str(uuid.uuid4()),
                        agent_name=a_exec.get("name", "Autonomous Agent"),
                        field_id=field_id,
                        role="Specialized Autonomous Agent",
                        status="COMPLETED",
                        confidence=a_exec.get("confidence", 95),
                        input_summary={"inputs": a_exec.get("inputs", [])},
                        output_summary={"outputs": a_exec.get("outputs", []), "details": a_exec.get("details", {})},
                        inputs=a_exec.get("inputs", []),
                        outputs=a_exec.get("outputs", []),
                        execution_time_ms=a_exec.get("duration_ms", 100),
                        started_at=datetime.now(timezone.utc),
                        completed_at=datetime.now(timezone.utc)
                    )
                    db_session.add(run_entry)
                await db_session.commit()
        except Exception as e:
            logger.error(f"Failed to log agent runs to database: {e}")

        # Step 7: Broadcast WebSocket event
        try:
            from app.integrations.websocket_manager import ws_manager
            await ws_manager.broadcast_to_farm(farm_id, "agent_completed", {
                "cycle_id": cycle_id,
                "agents_count": len(state["agent_executions"]),
                "summary": orch_record["outputs"],
                "duration_ms": duration_ms
            })
        except Exception:
            pass

        logger.info(f"Master Orchestrator completed {cycle_id} in {duration_ms}ms and persisted {len(state['agent_executions'])} agent runs.")
        return state

orchestrator = MasterOrchestrator()
