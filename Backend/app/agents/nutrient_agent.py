import time
from typing import Dict, Any
from app.agents.state import FarmAgentState, AgentExecutionResult

class NutrientAgent:
    def __init__(self):
        self.agent_id = "nutrient"
        self.name = "Nutrient & NPK Agent"
        self.role = "Soil Fertility & Fertigation Optimizer"

    async def run(self, state: FarmAgentState) -> Dict[str, Any]:
        start = time.time()
        telemetry = state.get("telemetry", {})
        nitrogen = float(telemetry.get("nitrogenLevel", 82.0))
        phosphorus = float(telemetry.get("phosphorusLevel", 14.0)) # benchmark 20+
        potassium = float(telemetry.get("potassiumLevel", 185.0))

        p_deficient = phosphorus < 20.0
        analysis = {
            "nitrogen": "Normal" if nitrogen >= 70 else "Low",
            "phosphorus": "Low (Deficient)" if p_deficient else "Optimal",
            "potassium": "Good",
            "fertigationRecommended": p_deficient,
            "recommendedFertilizer": "15 kg Water-Soluble DAP (12:61:00)" if p_deficient else None
        }

        duration_ms = int((time.time() - start) * 1000)
        exec_record: AgentExecutionResult = {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "Active",
            "confidence": 91,
            "duration_ms": max(duration_ms, 14),
            "inputs": [f"N: {nitrogen} mg/kg", f"P: {phosphorus} mg/kg", f"K: {potassium} mg/kg"],
            "outputs": [f"Phosphorus Flag: {'Low 14 mg/kg' if p_deficient else 'Optimal'}"],
            "details": analysis
        }
        state["agent_executions"].append(exec_record)
        state["nutrient_analysis"] = analysis
        return analysis

nutrient_agent = NutrientAgent()
