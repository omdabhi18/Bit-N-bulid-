import time
from typing import Dict, Any
from app.agents.state import FarmAgentState, AgentExecutionResult

class CropAgent:
    def __init__(self):
        self.agent_id = "crop"
        self.name = "Crop Phenology & Health Agent"
        self.role = "Growth Stage & Yield Optimization"

    async def run(self, state: FarmAgentState) -> Dict[str, Any]:
        start = time.time()
        crop_info = state.get("crop_info", {})
        crop_name = crop_info.get("name", "BT Cotton (કપાસ)")
        stage = crop_info.get("stage", "Flowering & Boll Formation")

        # Flowering stage is critical for cotton yield: water stress causes shedding
        is_critical_stage = "flowering" in stage.lower() or "boll" in stage.lower()

        analysis = {
            "crop": crop_name,
            "stage": stage,
            "waterSensitivityIndex": 0.88 if is_critical_stage else 0.45,
            "phenologyVulnerability": "High" if is_critical_stage else "Normal"
        }

        duration_ms = int((time.time() - start) * 1000)
        exec_record: AgentExecutionResult = {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "Active",
            "confidence": 89,
            "duration_ms": max(duration_ms, 18),
            "inputs": [f"Crop: {crop_name}", f"Stage: {stage}", "GDD: 1120"],
            "outputs": [f"Stage: {stage}", "Critical water stress vulnerability: High"],
            "details": analysis
        }
        state["agent_executions"].append(exec_record)
        state["crop_analysis"] = analysis
        return analysis

crop_agent = CropAgent()
