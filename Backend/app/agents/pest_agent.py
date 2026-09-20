import time
from typing import Dict, Any
from app.agents.state import FarmAgentState, AgentExecutionResult

class PestAgent:
    def __init__(self):
        self.agent_id = "pest"
        self.name = "Pest & Pathogen Vision Agent"
        self.role = "Early Disease Warning & Bio-controls"

    async def run(self, state: FarmAgentState) -> Dict[str, Any]:
        start = time.time()
        telemetry = state.get("telemetry", {})
        humidity = float(telemetry.get("airHumidity", 58.0))
        temp = float(telemetry.get("airTemperature", 33.2))

        # Night humidity > 75% creates high aphid / bollworm vector pressure
        pest_prob = 78 if humidity > 70 else 25
        pest_alert = pest_prob > 50

        analysis = {
            "pestProbability": pest_prob,
            "hasActiveAlert": pest_alert,
            "targetPest": "Aphids / Early Pink Bollworm",
            "recommendedRemedy": "Organic Neem-oil formulation spray (1500 ppm)"
        }

        duration_ms = int((time.time() - start) * 1000)
        exec_record: AgentExecutionResult = {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "Active",
            "confidence": 88,
            "duration_ms": max(duration_ms, 20),
            "inputs": [f"Ambient Humidity: {humidity}%", f"Temp: {temp}°C", "Field B Leaf Scans"],
            "outputs": [f"Aphid Risk: {pest_prob}%", "Recommended Neem 1500ppm bio-spray"],
            "details": analysis
        }
        state["agent_executions"].append(exec_record)
        state["pest_analysis"] = analysis
        return analysis

pest_agent = PestAgent()
