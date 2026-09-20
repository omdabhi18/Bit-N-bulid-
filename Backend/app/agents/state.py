from typing import TypedDict, List, Dict, Any, Optional

class AgentExecutionResult(TypedDict):
    agent_id: str
    name: str
    status: str
    confidence: int
    duration_ms: int
    inputs: List[str]
    outputs: List[str]
    details: Dict[str, Any]

class FarmAgentState(TypedDict):
    farm_id: str
    field_id: str
    telemetry: Dict[str, Any]
    crop_info: Dict[str, Any]
    weather_info: Dict[str, Any]
    market_info: Dict[str, Any]
    
    # Intermediate outputs
    soil_analysis: Optional[Dict[str, Any]]
    weather_analysis: Optional[Dict[str, Any]]
    crop_analysis: Optional[Dict[str, Any]]
    pest_analysis: Optional[Dict[str, Any]]
    nutrient_analysis: Optional[Dict[str, Any]]
    market_analysis: Optional[Dict[str, Any]]
    
    # Synthesized outcomes
    detected_risks: List[Dict[str, Any]]
    advisories: List[Dict[str, Any]]
    generated_plans: List[Dict[str, Any]]
    
    # Audit & Diagnostics
    agent_executions: List[AgentExecutionResult]
    errors: List[str]
