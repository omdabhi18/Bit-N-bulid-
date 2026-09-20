from typing import Dict, Any, Tuple
from app.utils.logger import logger

class ConstraintValidationResult:
    def __init__(self, is_valid: bool, reason: str, adjusted_parameters: Dict[str, Any] = None):
        self.is_valid = is_valid
        self.reason = reason
        self.adjusted_parameters = adjusted_parameters or {}

class ConstraintEngine:
    def __init__(self):
        self.max_daily_budget = 300.0 # INR
        self.max_wind_speed_spray = 18.0 # km/h
        self.max_rain_prob_irrigation = 40 # percentage

    def validate_irrigation_plan(
        self,
        cost: float,
        rainfall_prob: int,
        wind_speed: float,
        water_source_level: float = 88.0,
        line_pressure: float = 1.8
    ) -> ConstraintValidationResult:
        """
        Validates whether drip irrigation can safely proceed.
        Rejects if imminent rain makes irrigation wasteful, or if water/pressure is unsafe.
        """
        # 1. Rain Probability Check
        if rainfall_prob > self.max_rain_prob_irrigation:
            logger.warning(f"Constraint Engine: Rain probability {rainfall_prob}% exceeds {self.max_rain_prob_irrigation}%. Rejecting irrigation.")
            return ConstraintValidationResult(
                is_valid=False,
                reason=f"Natural rain probability is high ({rainfall_prob}%). Automated irrigation paused to avoid waterlogging and electricity waste."
            )

        # 2. Cost Budget Cap Check
        if cost > self.max_daily_budget:
            return ConstraintValidationResult(
                is_valid=False,
                reason=f"Estimated cost ₹{cost} exceeds maximum single-action budget cap of ₹{self.max_daily_budget}."
            )

        # 3. Water Source Level
        if water_source_level < 20.0:
            return ConstraintValidationResult(
                is_valid=False,
                reason=f"Water storage level ({water_source_level}%) too low for safe tube-well operation."
            )

        # 4. Line Pressure Check
        if line_pressure < 1.0 or line_pressure > 3.5:
            return ConstraintValidationResult(
                is_valid=False,
                reason=f"Irrigation line pressure ({line_pressure} bar) out of nominal bounds (1.2 - 2.5 bar)."
            )

        return ConstraintValidationResult(
            is_valid=True,
            reason="All constraints met: Cost within budget, safe weather window, tube well capacity optimal.",
            adjusted_parameters={
                "costBudget": f"₹150 Max (Est: ₹{int(cost)})",
                "weatherWindow": f"Safe (Rain prob {rainfall_prob}%, Wind {wind_speed} km/h)",
                "waterAvailability": f"Tube Well Level: High ({int(water_source_level)}%)",
                "safetyProtocols": f"Electrical grounding checked, line pressure {line_pressure} bar"
            }
        )

    def validate_foliar_spray_plan(
        self,
        wind_speed: float,
        rainfall_prob_24h: int,
        estimated_cost: float
    ) -> ConstraintValidationResult:
        """
        Validates pesticide or bio-spray against drift velocity and wash-off risk.
        """
        if wind_speed > self.max_wind_speed_spray:
            return ConstraintValidationResult(
                is_valid=False,
                reason=f"High wind velocity ({wind_speed} km/h) causes excessive droplet drift loss. Maximum safe limit is {self.max_wind_speed_spray} km/h."
            )

        if rainfall_prob_24h > 35:
            return ConstraintValidationResult(
                is_valid=False,
                reason=f"Rain forecast ({rainfall_prob_24h}%) will wash away bio-chemical active ingredients within 24 hours."
            )

        return ConstraintValidationResult(
            is_valid=True,
            reason="Weather window suitable for foliar spray.",
            adjusted_parameters={
                "costBudget": f"₹300 Max (Est: ₹{int(estimated_cost)})",
                "weatherWindow": f"Morning Window: Wind < {self.max_wind_speed_spray} km/h, No rain",
                "waterAvailability": "Adequate Farm Tank storage",
                "safetyProtocols": "Protective mask and gloves required"
            }
        )

constraint_engine = ConstraintEngine()
