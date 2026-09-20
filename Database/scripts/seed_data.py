import asyncio
import sys
import os
import hashlib
from datetime import datetime, timezone, timedelta

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Database.connection import AsyncSessionLocal, async_engine, Base
from Database.models import (
    User, UserRole, Farm, Field, Crop, Sensor, SensorReading,
    WeatherData, MarketPrice, Risk, AIAdvisory, ActionPlan,
    Task, DiseaseAnalysis, ExpertRequest, AgentRun, Alert, Notification, ActivityLog
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("krishinetra.db_seed")

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

async def seed_production_database():
    logger.info("Initializing schema...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Check if already seeded
        from sqlalchemy.future import select
        res = await session.execute(select(User).filter(User.email == "kishanbhai@greenvalley.in"))
        if res.scalars().first():
            logger.info("GreenValley Farm seed data already present. Skipping.")
            return

        logger.info("Seeding GreenValley Smart Farms (Rajkot, Gujarat)...")

        # 1. User
        user = User(
            id="usr-kishanbhai",
            name="Kishanbhai Patel",
            email="kishanbhai@greenvalley.in",
            phone="+91 98250 12345",
            password_hash=hash_pw("Password123!"),
            role=UserRole.FARMER.value,
            is_active=True
        )
        session.add(user)

        # 2. Farm
        farm = Farm(
            id="farm-greenvalley-01",
            owner_id="usr-kishanbhai",
            name="GreenValley Smart Farms",
            farmer_name="Kishanbhai Patel",
            village="Ribda",
            taluka="Gondal",
            district="Rajkot",
            state="Gujarat",
            latitude=21.9619,
            longitude=70.7923,
            area=12.5,
            soil_type="Medium Black Clayey Loam (કાળી જમીન)",
            irrigation_method="Drip Automation + Tube Well"
        )
        session.add(farm)

        # 3. Fields (Field A, Field B, Field C)
        fields = [
            Field(
                id="field-a",
                farm_id="farm-greenvalley-01",
                name="Field A - South Valley",
                area=5.2,
                crop_name="BT Cotton (કપાસ)",
                stage="Flowering (ફૂલ અવસ્થા)",
                health_score=78,
                soil_moisture=31.0,
                status="WARNING",
                risk_category="Water Stress",
                pest_risk="Low (15%)",
                soil_ph=6.8,
                nitrogen="Normal",
                phosphorus="Optimal",
                potassium="High",
                boundary=[
                    {"lat": 21.9635, "lng": 70.7910},
                    {"lat": 21.9645, "lng": 70.7938},
                    {"lat": 21.9615, "lng": 70.7945},
                    {"lat": 21.9605, "lng": 70.7915}
                ],
                color="#eab308",
                drip_status="Ready",
                recommendation="Irrigation required within 6 hours (2,500 L)"
            ),
            Field(
                id="field-b",
                farm_id="farm-greenvalley-01",
                name="Field B - North Ridge",
                area=4.1,
                crop_name="Sharbati Wheat (ઘઉં)",
                stage="Tillering (કૂટ અવસ્થા)",
                health_score=71,
                soil_moisture=48.0,
                status="CRITICAL",
                risk_category="Pest Risk & Phosphorus Deficiency",
                pest_risk="High (78%) - Pink Bollworm / Aphid alert",
                soil_ph=7.2,
                nitrogen="Optimal",
                phosphorus="Low ⚠️ (14 mg/kg)",
                potassium="Normal",
                boundary=[
                    {"lat": 21.9650, "lng": 70.7942},
                    {"lat": 21.9670, "lng": 70.7968},
                    {"lat": 21.9642, "lng": 70.7982},
                    {"lat": 21.9628, "lng": 70.7950}
                ],
                color="#ef4444",
                drip_status="Standby",
                recommendation="Pest inspection and DAP fertilizer soil dressing required"
            ),
            Field(
                id="field-c",
                farm_id="farm-greenvalley-01",
                name="Field C - East Plot",
                area=3.2,
                crop_name="Groundnut (મગફળી)",
                stage="Pod Development (સૂયા બેસવાની અવસ્થા)",
                health_score=92,

                soil_moisture=52.0,
                status="HEALTHY",
                risk_category="Optimal Conditions",
                pest_risk="None (8%)",
                soil_ph=6.9,
                nitrogen="Good",
                phosphorus="Optimal",
                potassium="Optimal",
                boundary=[
                    {"lat": 21.9600, "lng": 70.7890},
                    {"lat": 21.9620, "lng": 70.7905},
                    {"lat": 21.9595, "lng": 70.7930},
                    {"lat": 21.9580, "lng": 70.7900}
                ],
                color="#22c55e",
                drip_status="Optimal",
                recommendation="Conditions ideal. Next scheduled scouting in 3 days"
            )
        ]
        session.add_all(fields)

        # 4. Crops
        crops = [
            Crop(
                id="cotton",
                farm_id="farm-greenvalley-01",
                field_id="field-a",
                crop_name="BT Cotton (કપાસ)",
                variety="G.Cot.Hy-8",
                current_stage="Flowering & Boll Formation",
                area=5.2,
                sowing_date=datetime(2026, 6, 15, tzinfo=timezone.utc),
                expected_harvest_date=datetime(2026, 11, 20, tzinfo=timezone.utc),
            ),
            Crop(
                id="wheat",
                farm_id="farm-greenvalley-01",
                field_id="field-b",
                crop_name="Sharbati Wheat (ઘઉં)",
                variety="GW-496",
                current_stage="Vegetative Tillering",
                area=4.1,
                sowing_date=datetime(2026, 11, 10, tzinfo=timezone.utc),
                expected_harvest_date=datetime(2027, 3, 15, tzinfo=timezone.utc),
            ),
            Crop(
                id="groundnut",
                farm_id="farm-greenvalley-01",
                field_id="field-c",
                crop_name="Groundnut (મગફળી)",
                variety="GG-20",
                current_stage="Pod Development",
                area=3.2,
                sowing_date=datetime(2026, 7, 2, tzinfo=timezone.utc),
                expected_harvest_date=datetime(2026, 10, 25, tzinfo=timezone.utc),
            )
        ]
        session.add_all(crops)


        # 5. Sensors
        sensors = [
            Sensor(id="SN-Cotton-01", farm_id="farm-greenvalley-01", field_id="field-a", device_id="DEV-FDR-01", name="Soil & Microclimate Node A", sensor_type="SOIL_MOISTURE", battery=94, signal_strength="Excellent (4G IoT)", status="ONLINE", last_seen="1 minute ago"),
            Sensor(id="SN-Wheat-02", farm_id="farm-greenvalley-01", field_id="field-b", device_id="DEV-MULTI-02", name="Soil & Leaf Sensor Node B", sensor_type="TEMPERATURE", battery=88, signal_strength="Good (LoRaWAN)", status="ONLINE", last_seen="3 minutes ago"),
            Sensor(id="SN-Gnut-03", farm_id="farm-greenvalley-01", field_id="field-c", device_id="DEV-VALVE-03", name="Smart Drip Controller C", sensor_type="PH", battery=100, signal_strength="Solar Mains (WiFi)", status="ONLINE", last_seen="Just now"),
            Sensor(id="SN-Weather-04", farm_id="farm-greenvalley-01", field_id="field-a", device_id="DEV-WEATHER-04", name="Micro Weather Station", sensor_type="HUMIDITY", battery=98, signal_strength="Satellite IoT", status="ONLINE", last_seen="2 minutes ago")
        ]
        session.add_all(sensors)

        # 6. Sensor Readings (Time-series)
        now = datetime.now(timezone.utc)
        readings = [
            SensorReading(id="read-01", sensor_id="SN-Cotton-01", field_id="field-a", timestamp=now - timedelta(hours=6), soil_moisture=36.0, soil_temperature=24.0, soil_ph=6.8, soil_ec=0.41, nitrogen=82.0, phosphorus=14.0, potassium=185.0, air_temperature=28.0, air_humidity=70.0),
            SensorReading(id="read-02", sensor_id="SN-Cotton-01", field_id="field-a", timestamp=now - timedelta(hours=3), soil_moisture=33.0, soil_temperature=30.0, soil_ph=6.8, soil_ec=0.42, nitrogen=82.0, phosphorus=14.0, potassium=185.0, air_temperature=32.0, air_humidity=55.0),
            SensorReading(id="read-03", sensor_id="SN-Cotton-01", field_id="field-a", timestamp=now, soil_moisture=31.4, soil_temperature=27.8, soil_ph=6.8, soil_ec=0.42, nitrogen=82.0, phosphorus=14.0, potassium=185.0, air_temperature=33.2, air_humidity=58.0)
        ]
        session.add_all(readings)

        # 7. Weather Data
        weather = WeatherData(
            id="weather-rajkot-01",
            farm_id="farm-greenvalley-01",
            location="Rajkot, Gujarat",
            temperature=33.0,
            humidity=58.0,
            rainfall_probability=12,
            wind_speed=14.0,
            weather_condition="Mostly Sunny",
            uv_index=8,
            dew_point=22.0,
            et0="5.8 mm/day",
            advisory="Favorable conditions for drip irrigation this evening. Wind speed safe for low-drift activities."
        )
        session.add(weather)

        # 8. Market Prices
        prices = [
            MarketPrice(id="comm-cotton", crop="Shankar-6 Cotton (કપાસ)", mandi="Rajkot APMC", price=7380.0, unit="₹ / Quintal (100 kg)", change_7d=4.2, trend="UP", msp_price=7122.0, ai_recommendation="Favorable Selling Window. Prices at 4-week high due to export demand."),
            MarketPrice(id="comm-wheat", crop="Lokwan / Sharbati Wheat (ઘઉં)", mandi="Rajkot APMC", price=2850.0, unit="₹ / Quintal", change_7d=1.8, trend="UP", msp_price=2275.0, ai_recommendation="Hold Inventory. Government procurement starting soon."),
            MarketPrice(id="comm-groundnut", crop="Groundnut GG-20 (મગફળી)", mandi="Gondal APMC", price=6520.0, unit="₹ / Quintal", change_7d=-0.9, trend="DOWN", msp_price=6783.0, ai_recommendation="Sell at MSP Center if open; otherwise store.")
        ]
        session.add_all(prices)

        # 9. Risks
        risks = [
            Risk(
                id="risk-01",
                farm_id="farm-greenvalley-01",
                field_id="field-a",
                category="Water Stress (પાણીની અછત)",
                risk_type="WATER_STRESS",
                severity="HIGH",
                confidence=88,
                evidence=[
                    "Soil moisture dropped to 31% (critical wilting point: 28%)",
                    "Evapotranspiration rate elevated at 5.8 mm/day due to peak daytime temps",
                    "Flowering stage requires consistent 40-50% root-zone moisture"
                ],
                recommended_action="Targeted drip irrigation of 2,500 L at 18:00 hrs",
                status="ACTIVE",
                plan_generated=True,
                plan_id="PLAN-1024"
            ),
            Risk(
                id="risk-02",
                farm_id="farm-greenvalley-01",
                field_id="field-b",
                category="Pest Risk (જીવાત ઉપદ્રવ)",
                risk_type="PEST",
                severity="CRITICAL",
                confidence=78,
                evidence=[
                    "Nocturnal humidity > 78% combined with 22°C ambient favors aphid multiplication",
                    "Spectral imagery highlights leaf chlorosis in eastern sub-zone",
                    "Regional APMC pest advisory reports early bollworm emergence"
                ],
                recommended_action="Physical scouting + Organic Neem-oil formulation spray (1500 ppm)",
                status="ACTIVE",
                plan_generated=True,
                plan_id="PLAN-1025"
            )
        ]
        session.add_all(risks)

        # 10. AI Advisories
        adv = AIAdvisory(
            id="adv-01",
            farm_id="farm-greenvalley-01",
            field_id="field-a",
            risk_id="risk-01",
            title="Urgent Drip Irrigation for Cotton Field A",
            title_gu="કપાસ પ્લોટ A માં તાત્કાલિક ડ્રિપ પિયત આપવું",
            title_hi="कपास खेत A में तुरंत ड्रिप सिंचाई करें",
            recommendation="Execute drip irrigation today between 6:00 PM and 8:00 PM.",
            reasoning="Moisture deficit in flowering stage. Rain probability is only 12%.",
            priority="High",
            confidence=91,
            status="PENDING_APPROVAL",
            orchestrator_summary="Water stress detected in flowering crop stage. AI recommends executing irrigation today between 6:00 PM and 8:00 PM.",
            explainability={
                "factors": [
                    {"name": "Current Root Moisture", "value": "31.4%", "impact": "Severe Deficit", "threshold": "Target 45%"},
                    {"name": "Rainfall Probability 24h", "value": "12%", "impact": "No Natural Rain Expected", "threshold": "< 30%"}
                ],
                "whyText": "Root moisture fell below wilting benchmark with minimal natural rain expected."
            },
            action_details={
                "action": "Drip Irrigation",
                "volume": "2,500 Liters",
                "duration": "35 Minutes",
                "costEstimate": "₹45 (Electricity)",
                "waterSource": "North Tube Well"
            }
        )
        session.add(adv)

        # 11. Action Plans
        plan = ActionPlan(
            id="PLAN-1024",
            farm_id="farm-greenvalley-01",
            field_id="field-a",
            risk_id="risk-01",
            advisory_id="adv-01",
            title="Precision Water Stress Alleviation",
            target_field="Field A (Cotton - 5.2 Acres)",
            action="Automated Drip Irrigation",
            action_type="Automated Drip Irrigation",
            scheduled_time="Today • 18:00 - 18:35 IST",
            duration="35 Minutes",
            estimated_cost=45.0,
            water_volume="2,500 L",
            constraints={
                "costBudget": "₹150 Max (Est: ₹45)",
                "weatherWindow": "Safe (Rain prob 12%, Wind 14 km/h)",
                "waterAvailability": "Tube Well Level: High (88%)",
                "safetyProtocols": "Electrical grounding checked, line pressure 1.8 bar"
            },
            status="APPROVED"
        )
        session.add(plan)

        # 12. Tasks
        task = Task(
            id="TSK-01",
            farm_id="farm-greenvalley-01",
            field_id="field-a",
            action_plan_id="PLAN-1024",
            title="Trigger Drip Irrigation in Field A",
            description="Run for 35 mins. Auto-shutoff when soil moisture reaches 44%.",
            status="TODO",
            priority="High",
            due_at="Today 18:00",
            icon="Droplets"
        )
        session.add(task)

        # 13. Disease Analyses
        disease = DiseaseAnalysis(
            id="dis-01",
            field_id="field-a",
            crop="Cotton (કપાસ)",
            disease="Cotton Leaf Curl Virus & Bacterial Blight",
            disease_name="Cotton Leaf Curl Virus & Bacterial Blight",
            disease_name_gu="કપાસના પાન વળવાનો રોગ અને બેક્ટેરિયલ બ્લાઇટ",
            confidence=88,
            severity="High",
            image_url="https://images.unsplash.com/photo-1599818490533-3d0d540df167?auto=format&fit=crop&w=800&q=80",
            symptoms=["Upward curling and thickening of leaf veins", "Angular water-soaked spots"],
            recommended_remedy={"organic": "5% Neem Seed Kernel Extract (NSKE)", "chemical": "Streptocycline (100 ppm)"}
        )
        session.add(disease)

        # 14. Expert Requests
        expert_req = ExpertRequest(
            id="ESC-801",
            field_id="field-b",
            disease_analysis_id="dis-01",
            risk_id="risk-02",
            issue="Unusual Yellow Leaf Tip Necrosis with Low AI Confidence (58%)",
            ai_confidence=58,
            reason="Micro-image glare and overlapping fungal vs micronutrient symptoms",
            assigned_expert="Dr. Arvind Dave (Senior Agronomist, JAU Junagadh)",
            status="REVIEW_PENDING"
        )
        session.add(expert_req)

        # 15. Agent Runs
        agent_runs = [
            AgentRun(id="run-01", agent_name="MASTER_ORCHESTRATOR", status="COMPLETED", confidence=96, input_summary="Telemetry + Weather + Phenology", output_summary="Plan #1024 Generated"),
            AgentRun(id="run-02", agent_name="SOIL_AGENT", status="COMPLETED", confidence=94, input_summary="Moisture 31.4%", output_summary="Deficit Alert flagged"),
            AgentRun(id="run-03", agent_name="WEATHER_AGENT", status="COMPLETED", confidence=92, input_summary="Rain prob 12%", output_summary="Safe spray and watering window")
        ]
        session.add_all(agent_runs)

        # 16. Alerts
        alert = Alert(
            id="alt-01",
            user_id="usr-kishanbhai",
            field_id="field-a",
            type="WATER_DEFICIT",
            severity="WARNING",
            title="Field A Root Moisture Below Benchmark",
            message="Soil moisture has fallen to 31.4%. Drip irrigation recommended."
        )
        session.add(alert)

        # 17. Notifications
        notification = Notification(
            id="notif-01",
            user_id="usr-kishanbhai",
            channel="SMS",
            title="Drip Irrigation Ready",
            message="Plan #1024 ready for approval in Field A."
        )
        session.add(notification)

        # 18. Activity Logs
        logs = [
            ActivityLog(id="LOG-01", user_id="usr-kishanbhai", farm_id="farm-greenvalley-01", field_id="field-a", agent="Farmer Interaction", event="Farmer approved Plan #1024 (Drip Irrigation)", severity="success"),
            ActivityLog(id="LOG-02", user_id="usr-kishanbhai", farm_id="farm-greenvalley-01", field_id="field-a", agent="Master Orchestrator", event="Generated Action Plan #1024 with cost constraint ₹45", severity="info"),
            ActivityLog(id="LOG-03", user_id="usr-kishanbhai", farm_id="farm-greenvalley-01", field_id="field-a", agent="Meteorological Agent", event="Scanned radar: rain probability 12% (safe for watering)", severity="info"),
            ActivityLog(id="LOG-04", user_id="usr-kishanbhai", farm_id="farm-greenvalley-01", field_id="field-a", agent="Soil & Moisture Agent", event="Detected Root Deficit: Field A moisture 31.4% < threshold", severity="warning")
        ]
        session.add_all(logs)

        await session.commit()
        logger.info("All 18 entities successfully seeded into PostgreSQL/SQLite database!")

if __name__ == "__main__":
    asyncio.run(seed_production_database())
