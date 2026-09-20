import time
from typing import Dict, Any, List
from app.agents.state import FarmAgentState, AgentExecutionResult
from app.agents.constraint_engine import constraint_engine
from app.agents.llm_provider import get_llm_provider
from app.utils.logger import logger

class ConstrainedActionPlanner:
    def __init__(self):
        self.agent_id = "planner"
        self.name = "Constrained Action Planner"
        self.role = "Constraint Solver (Cost, Weather, Resources)"
        self.llm = get_llm_provider()

    async def run(self, state: FarmAgentState) -> List[Dict[str, Any]]:
        start = time.time()
        risks = state.get("detected_risks", [])
        weather = state.get("weather_info", {})
        telemetry = state.get("telemetry", {})

        rain_prob = int(weather.get("rainfallProb24h", 12))
        wind_speed = float(weather.get("windSpeed", 14.0))

        action_plans = []
        advisories = []

        # Process primary Water Stress Risk
        water_risk = next((r for r in risks if "Water Stress" in r.get("category", "")), None)
        if water_risk:
            # Validate via ConstraintEngine
            validation = constraint_engine.validate_irrigation_plan(
                cost=45.0,
                rainfall_prob=rain_prob,
                wind_speed=wind_speed,
                water_source_level=88.0,
                line_pressure=1.8
            )

            if validation.is_valid:
                plan_1024 = {
                    "id": "PLAN-1024",
                    "title": "Precision Water Stress Alleviation",
                    "targetField": "Field A (Cotton - 5.2 Acres)",
                    "actionType": "Automated Drip Irrigation",
                    "scheduledTime": "Today • 18:00 - 18:35 IST",
                    "status": "Approved",
                    "priority": "High",
                    "estimatedCost": 45.0,
                    "waterVolume": "2,500 L",
                    "constraints": validation.adjusted_parameters,
                    "hardwareTarget": "Solenoid Valve SV-01 (Field A)",
                    "assignedTo": "Automated IoT Valve + Kishanbhai"
                }
                action_plans.append(plan_1024)

                # Generate explainability via LLM
                why_text = await self.llm.generate_explanation(water_risk, telemetry)

                advisories.append({
                    "id": "adv-01",
                    "title": "Urgent Drip Irrigation for Cotton Field A",
                    "titleGu": "કપાસ પ્લોટ A માં તાત્કાલિક ડ્રિપ પિયત આપવું",
                    "titleHi": "कपास खेत A में तुरंत ड्रिप सिंचाई करें",
                    "field": "Field A (Cotton)",
                    "priority": "High",
                    "confidenceScore": 91,
                    "status": "Pending Approval",
                    "timestamp": "10:15 AM Today",
                    "orchestratorSummary": "Water stress detected in flowering crop stage. AI recommends executing irrigation today between 6:00 PM and 8:00 PM.",
                    "explainability": {
                        "factors": [
                            { "name": "Current Root Moisture", "value": f"{telemetry.get('soilMoisture', 31.4)}%", "impact": "Severe Deficit", "threshold": "Target 45%" },
                            { "name": "Rainfall Probability 24h", "value": f"{rain_prob}%", "impact": "No Natural Rain Expected", "threshold": "< 30%" },
                            { "name": "Daytime Soil Temp", "value": f"{telemetry.get('soilTemperature', 27.8)}°C", "impact": "High Transpiration Loss", "threshold": "Normal < 30°C" },
                            { "name": "Phenological Crop Stage", "value": "Flowering & Boll", "impact": "Critical Yield Sensitivity", "threshold": "Peak Water Need" }
                        ],
                        "whyText": why_text
                    },
                    "actionDetails": {
                        "action": "Drip Irrigation",
                        "volume": "2,500 Liters",
                        "duration": "35 Minutes",
                        "zone": "Field A - Zone 2 Solenoid",
                        "costEstimate": "₹45 (Electricity)",
                        "waterSource": "North Tube Well"
                    }
                })

        # Process Pest Risk
        pest_risk = next((r for r in risks if "Pest" in r.get("category", "")), None)
        if pest_risk:
            spray_validation = constraint_engine.validate_foliar_spray_plan(
                wind_speed=wind_speed,
                rainfall_prob_24h=rain_prob,
                estimated_cost=180.0
            )
            if spray_validation.is_valid:
                action_plans.append({
                    "id": "PLAN-1025",
                    "title": "Organic Pest Intervention Protocol",
                    "targetField": "Field B (Wheat - 4.1 Acres)",
                    "actionType": "Bio-Pesticide Spraying",
                    "scheduledTime": "Tomorrow • 07:30 - 08:30 IST",
                    "status": "Scheduled",
                    "priority": "High",
                    "estimatedCost": 180.0,
                    "waterVolume": "200 L Mix",
                    "constraints": spray_validation.adjusted_parameters,
                    "hardwareTarget": "Battery Sprayer Kit #2",
                    "assignedTo": "Field Worker: Ramesh Patel"
                })

        duration_ms = int((time.time() - start) * 1000)
        exec_record: AgentExecutionResult = {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": "Active",
            "confidence": 93,
            "duration_ms": max(duration_ms, 25),
            "inputs": ["Risk Priority Matrix", "Constraint validation results", "Cost models"],
            "outputs": [f"Synthesized {len(action_plans)} constrained action plans", "Plan #1024 parameters locked (35 mins, ₹45)"],
            "details": {"plansCount": len(action_plans)}
        }
        state["agent_executions"].append(exec_record)
        state["generated_plans"] = action_plans
        state["advisories"] = advisories
        return action_plans

action_planner = ConstrainedActionPlanner()
