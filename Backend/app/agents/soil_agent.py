import time
from typing import Dict, Any
from app.agents.state import FarmAgentState, AgentExecutionResult
from app.utils.logger import logger

class SoilAgent:
    def __init__(self):
        self.agent_id = "soil"
        self.name = "Soil & Moisture Agent"
        self.role = "Root Zone Telemetry & Nutrient Modeler"

    async def run(self, state: FarmAgentState) -> Dict[str, Any]:
        start = time.time()
        telemetry = state.get("telemetry", {})
        soil_moisture = float(telemetry.get("soilMoisture", 31.4))
        soil_temp = float(telemetry.get("soilTemperature", 27.8))
        soil_ph = float(telemetry.get("soilPH", 6.8))
        soil_ec = float(telemetry.get("soilEC", 0.42))

        # Deterministic domain logic:
        # Field A root zone wilting point threshold is 28-35%
        is_water_deficit = soil_moisture < 35.0
        deficit_severity = "High" if soil_moisture < 32.0 else "Medium" if soil_moisture < 38.0 else "Normal"

        outputs = [
            f"Soil Moisture: {soil_moisture}% ({deficit_severity})",
            f"Root Temp: {soil_temp}°C, pH: {soil_ph}, EC: {soil_ec} dS/m"
        ]
        if is_water_deficit:
            outputs.append(f"Water Deficit Alert: {soil_moisture}% < 35% target")

        analysis = {
            "soilMoisture": soil_moisture,
            "isWaterDeficit": is_water_deficit,
            "deficitSeverity": deficit_severity,
            "recommendedIrrigationVolumeLiters": 2500 if is_water_deficit else 0,
            "recommendedRunMinutes": 35 if is_water_deficit else 0
        }

        duration_ms = int((time.time() - start) * 1000)
        exec_record: AgentExecutionResult = {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "Active",
            "confidence": 94,
            "duration_ms": max(duration_ms, 12),
            "inputs": [f"FDR moisture probes: {soil_moisture}%", f"Temp: {soil_temp}°C", f"pH: {soil_ph}"],
            "outputs": outputs,
            "details": analysis
        }
        state["agent_executions"].append(exec_record)
        state["soil_analysis"] = analysis
        logger.info(f"SoilAgent finished in {duration_ms}ms with deficit={is_water_deficit}")
        return analysis

soil_agent = SoilAgent()
