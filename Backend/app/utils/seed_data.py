from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.models.farm import Farm, Field
from app.models.crop import Crop
from app.models.sensor import SensorNode, SensorReading
from app.models.risk import Risk
from app.models.advisory import AIAdvisory
from app.models.action_plan import ActionPlan
from app.models.task import FarmTask
from app.models.disease import DiseaseAnalysis, ExpertReviewTicket
from app.models.weather import WeatherRecord
from app.models.market import MarketCommodity
from app.models.audit import ActivityLog
from app.utils.security import get_password_hash
from app.utils.logger import logger

async def seed_database(db: AsyncSession):
    # Check if already seeded
    existing_user = await db.execute(select(User).filter(User.email == "kishanbhai@greenvalley.in"))
    if existing_user.scalars().first():
        logger.info("Database already seeded. Skipping seed.")
        return

    logger.info("Seeding realistic database models for GreenValley Smart Farms...")

    # 1. User
    user = User(
        id="usr-kishanbhai",
        email="kishanbhai@greenvalley.in",
        phone="+91 98250 12345",
        full_name="Kishanbhai Patel",
        hashed_password=get_password_hash("Password123!"),
        role="farmer",
        is_active=True
    )
    db.add(user)

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
        total_area_acre=12.5,
        soil_type="Medium Black Clayey Loam (કાળી જમીન)",
        irrigation_method="Drip Automation + Tube Well",
        latitude=21.9619,
        longitude=70.7923
    )
    db.add(farm)

    # 3. Fields
    fields = [
        Field(
            id="field-a",
            farm_id="farm-greenvalley-01",
            name="Field A - South Valley",
            crop="BT Cotton (કપાસ)",
            area="5.2 Acres",
            stage="Flowering (ફૂલ અવસ્થા)",
            health_score=78,
            soil_moisture=31.0,
            status="Warning",
            risk_category="Water Stress",
            pest_risk="Low (15%)",
            soil_ph=6.8,
            nitrogen="Normal",
            phosphorus="Optimal",
            potassium="High",
            sensor_node="SN-Cotton-01",
            sensor_status="Online",
            coordinates=[
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
            crop="Sharbati Wheat (ઘઉં)",
            area="4.1 Acres",
            stage="Tillering (કૂટ અવસ્થા)",
            health_score=71,
            soil_moisture=48.0,
            status="Critical",
            risk_category="Pest Risk & Phosphorus Deficiency",
            pest_risk="High (78%) - Pink Bollworm / Aphid alert",
            soil_ph=7.2,
            nitrogen="Optimal",
            phosphorus="Low ⚠️ (14 mg/kg)",
            potassium="Normal",
            sensor_node="SN-Wheat-02",
            sensor_status="Online",
            coordinates=[
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
            crop="Groundnut (મગફળી)",
            area="3.2 Acres",
            stage="Pod Development (સૂયા બેસવાની અવસ્થા)",
            health_score=92,
            soil_moisture=52.0,
            status="Healthy",
            risk_category="Optimal Conditions",
            pest_risk="None (8%)",
            soil_ph=6.9,
            nitrogen="Good",
            phosphorus="Optimal",
            potassium="Optimal",
            sensor_node="SN-Gnut-03",
            sensor_status="Online",
            coordinates=[
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
    db.add_all(fields)

    # 4. Crops (Full 24 standardized crops)
    crops_catalog_data = [
        {"id": "cotton", "name": "Cotton", "name_gujarati": "કપાસ", "category": "Cash Crop", "scientific_name": "Gossypium hirsutum", "disease_ai_supported": True, "variety": "BT Cotton RCH-2 / G.Cot.Hy-8", "stage": "Flowering & Boll Formation", "area": 5.2, "field_name": "Field A"},
        {"id": "wheat", "name": "Wheat", "name_gujarati": "ઘઉં", "category": "Cereal", "scientific_name": "Triticum aestivum", "disease_ai_supported": True, "variety": "GW-496 / Sharbati", "stage": "Tillering (કૂટ અવસ્થા)", "area": 4.1, "field_name": "Field B"},
        {"id": "tomato", "name": "Tomato", "name_gujarati": "ટામેટા", "category": "Vegetable", "scientific_name": "Solanum lycopersicum", "disease_ai_supported": True, "variety": "Abhinav / US-440", "stage": "Fruiting & Ripening", "area": 2.5, "field_name": "Field D"},
        {"id": "groundnut", "name": "Groundnut", "name_gujarati": "મગફળી", "category": "Oilseed", "scientific_name": "Arachis hypogaea", "disease_ai_supported": True, "variety": "GG-20 / GJG-32", "stage": "Pod Development (સૂયા બેસવાની અવસ્થા)", "area": 3.2, "field_name": "Field C"},
        {"id": "rice", "name": "Rice", "name_gujarati": "ડાંગર", "category": "Cereal", "scientific_name": "Oryza sativa", "disease_ai_supported": True, "variety": "Gurjari / GR-11", "stage": "Tillering / Panicle Initiation", "area": 4.0, "field_name": "Plot R"},
        {"id": "maize", "name": "Maize", "name_gujarati": "મકાઈ", "category": "Cereal", "scientific_name": "Zea mays", "disease_ai_supported": True, "variety": "African Tall / Sweet Corn", "stage": "Tasseling & Silking", "area": 3.0, "field_name": "Plot M"},
        {"id": "bajra", "name": "Bajra", "name_gujarati": "બાજરી", "category": "Millet", "scientific_name": "Pennisetum glaucum", "disease_ai_supported": False, "variety": "GHB-558", "stage": "Grain Formation", "area": 2.0, "field_name": "Plot B"},
        {"id": "jowar", "name": "Jowar", "name_gujarati": "જુવાર", "category": "Millet", "scientific_name": "Sorghum bicolor", "disease_ai_supported": False, "variety": "Gundari / CSV-15", "stage": "Vegetative", "area": 2.0, "field_name": "Plot J"},
        {"id": "onion", "name": "Onion", "name_gujarati": "ડુંગળી", "category": "Vegetable", "scientific_name": "Allium cepa", "disease_ai_supported": True, "variety": "Pilipatti / Nashik Red", "stage": "Bulb Development", "area": 1.5, "field_name": "Plot O"},
        {"id": "potato", "name": "Potato", "name_gujarati": "બટાકા", "category": "Vegetable", "scientific_name": "Solanum tuberosum", "disease_ai_supported": True, "variety": "Kufri Badshah / Pukhraj", "stage": "Tuber Initiation", "area": 2.0, "field_name": "Plot P"},
        {"id": "chilli", "name": "Chilli", "name_gujarati": "મરચું", "category": "Vegetable", "scientific_name": "Capsicum annuum", "disease_ai_supported": True, "variety": "Resham Patti / G-4", "stage": "Flowering & Fruit Setting", "area": 1.0, "field_name": "Plot CH"},
        {"id": "brinjal", "name": "Brinjal", "name_gujarati": "રીંગણ", "category": "Vegetable", "scientific_name": "Solanum melongena", "disease_ai_supported": False, "variety": "Ravaiya / Doli-5", "stage": "Vegetative", "area": 1.0, "field_name": "Plot BR"},
        {"id": "okra", "name": "Okra", "name_gujarati": "ભીંડા", "category": "Vegetable", "scientific_name": "Abelmoschus esculentus", "disease_ai_supported": True, "variety": "Gujarat Okra-3 / Radhika", "stage": "Harvesting / Fruiting", "area": 1.0, "field_name": "Plot OK"},
        {"id": "cabbage", "name": "Cabbage", "name_gujarati": "કોબી", "category": "Vegetable", "scientific_name": "Brassica oleracea var. capitata", "disease_ai_supported": False, "variety": "Golden Acre", "stage": "Head Formation", "area": 1.0, "field_name": "Plot CB"},
        {"id": "cauliflower", "name": "Cauliflower", "name_gujarati": "ફૂલકોબી", "category": "Vegetable", "scientific_name": "Brassica oleracea var. botrytis", "disease_ai_supported": False, "variety": "Pusa Deepali / Snowball", "stage": "Curd Development", "area": 1.0, "field_name": "Plot CF"},
        {"id": "soybean", "name": "Soybean", "name_gujarati": "સોયાબીન", "category": "Oilseed", "scientific_name": "Glycine max", "disease_ai_supported": True, "variety": "JS-335 / NRC-37", "stage": "Pod Filling", "area": 3.0, "field_name": "Plot SB"},
        {"id": "sugarcane", "name": "Sugarcane", "name_gujarati": "શેરડી", "category": "Cash Crop", "scientific_name": "Saccharum officinarum", "disease_ai_supported": False, "variety": "Co-86032", "stage": "Grand Growth", "area": 5.0, "field_name": "Plot SC"},
        {"id": "chickpea", "name": "Chickpea", "name_gujarati": "ચણા", "category": "Pulse", "scientific_name": "Cicer arietinum", "disease_ai_supported": True, "variety": "Gujarat Gram-1 / Chana Dahod Yellow", "stage": "Pod Development", "area": 2.5, "field_name": "Plot CP"},
        {"id": "pigeon_pea", "name": "Pigeon Pea", "name_gujarati": "તુવેર", "category": "Pulse", "scientific_name": "Cajanus cajan", "disease_ai_supported": False, "variety": "Vaishali / BDN-2", "stage": "Flowering", "area": 2.0, "field_name": "Plot PP"},
        {"id": "sesame", "name": "Sesame", "name_gujarati": "તલ", "category": "Oilseed", "scientific_name": "Sesamum indicum", "disease_ai_supported": False, "variety": "Gujarat Til-2", "stage": "Capsule Formation", "area": 1.5, "field_name": "Plot SM"},
        {"id": "mustard", "name": "Mustard", "name_gujarati": "સરસવ", "category": "Oilseed", "scientific_name": "Brassica juncea", "disease_ai_supported": False, "variety": "Gujarat Mustard-3 / Pusa Bold", "stage": "Siliqua Formation", "area": 2.0, "field_name": "Plot MS"},
        {"id": "castor", "name": "Castor", "name_gujarati": "એરંડા", "category": "Oilseed", "scientific_name": "Ricinus communis", "disease_ai_supported": False, "variety": "GCH-7", "stage": "Primary Spike Maturity", "area": 3.0, "field_name": "Plot CS"},
        {"id": "green_gram", "name": "Green Gram", "name_gujarati": "મગ", "category": "Pulse", "scientific_name": "Vigna radiata", "disease_ai_supported": False, "variety": "GM-4", "stage": "Podding", "area": 1.5, "field_name": "Plot GG"},
        {"id": "black_gram", "name": "Black Gram", "name_gujarati": "અડદ", "category": "Pulse", "scientific_name": "Vigna mungo", "disease_ai_supported": False, "variety": "T-9 / GU-1", "stage": "Vegetative & Flowering", "area": 1.5, "field_name": "Plot BG"},
    ]
    crops = [
        Crop(
            id=c["id"],
            farm_id="farm-greenvalley-01",
            name=c["name"],
            name_gujarati=c["name_gujarati"],
            category=c["category"],
            scientific_name=c["scientific_name"],
            disease_ai_supported=c["disease_ai_supported"],
            is_active=True,
            variety=c["variety"],
            stage=c["stage"],
            area=c["area"],
            field_name=c["field_name"],
            sowing_date="2026-06-15"
        )
        for c in crops_catalog_data
    ]
    db.add_all(crops)

    # 5. Sensors
    sensors = [
        SensorNode(id="SN-Cotton-01", farm_id="farm-greenvalley-01", name="Soil & Microclimate Node A", field_name="Field A", battery=94, signal_strength="Excellent (4G IoT)", status="Online", last_sync="1 minute ago", sensor_type="FDR Moisture + NPK Probes"),
        SensorNode(id="SN-Wheat-02", farm_id="farm-greenvalley-01", name="Soil & Leaf Sensor Node B", field_name="Field B", battery=88, signal_strength="Good (LoRaWAN)", status="Online", last_sync="3 minutes ago", sensor_type="Soil Moisture + Multispectral Optical"),
        SensorNode(id="SN-Gnut-03", farm_id="farm-greenvalley-01", name="Smart Drip Controller C", field_name="Field C", battery=100, signal_strength="Solar Mains (WiFi)", status="Online", last_sync="Just now", sensor_type="Solenoid Valve + EC Sensor"),
        SensorNode(id="SN-Weather-04", farm_id="farm-greenvalley-01", name="Micro Weather Station", field_name="Central Farm", battery=98, signal_strength="Satellite IoT", status="Online", last_sync="2 minutes ago", sensor_type="Anemometer + Pyranometer + Rain Gauge")
    ]
    db.add_all(sensors)

    # 6. Risks
    risks = [
        Risk(
            id="risk-01",
            farm_id="farm-greenvalley-01",
            category="Water Stress (પાણીની અછત)",
            icon="Droplets",
            severity="High",
            field="Field A (Cotton)",
            probability=88,
            indicators=[
                "Soil moisture dropped to 31% (critical wilting point: 28%)",
                "Evapotranspiration rate elevated at 5.8 mm/day due to 34°C peak temp",
                "Flowering stage requires consistent 40-50% root-zone moisture"
            ],
            recommended_action="Targeted drip irrigation of 2,500 L at 18:00 hrs",
            plan_generated=True,
            plan_id="PLAN-1024"
        ),
        Risk(
            id="risk-02",
            farm_id="farm-greenvalley-01",
            category="Pest Risk (જીવાત ઉપદ્રવ)",
            icon="Bug",
            severity="Critical",
            field="Field B (Wheat)",
            probability=78,
            indicators=[
                "Nocturnal humidity > 78% combined with 22°C ambient favors aphid multiplication",
                "Spectral imagery highlights leaf chlorosis in eastern sub-zone",
                "Regional APMC pest advisory reports early bollworm emergence"
            ],
            recommended_action="Physical scouting + Organic Neem-oil formulation spray (1500 ppm)",
            plan_generated=True,
            plan_id="PLAN-1025"
        ),
        Risk(
            id="risk-03",
            farm_id="farm-greenvalley-01",
            category="Nutrient Deficiency (પોષક તત્વોની ખામી)",
            icon="Sprout",
            severity="Medium",
            field="Field B (Wheat)",
            probability=69,
            indicators=[
                "Phosphorus detected at 14 mg/kg (benchmark minimum is 22 mg/kg)",
                "Slow tillering root extension observed",
                "Soil EC remains within safe osmotic range (0.42 dS/m)"
            ],
            recommended_action="Apply 25 kg DAP or rock phosphate during next fertigation cycle",
            plan_generated=False,
            plan_id=None
        ),
        Risk(
            id="risk-04",
            farm_id="farm-greenvalley-01",
            category="Weather Risk (હવામાન અસર)",
            icon="CloudRain",
            severity="Medium",
            field="All Fields",
            probability=62,
            indicators=[
                "Sudden gusty winds (up to 32 km/h) forecasted for tomorrow afternoon",
                "Scattered drizzle probability 35% on Day 3",
                "Avoid foliar spraying during high wind velocity to prevent drift loss"
            ],
            recommended_action="Complete any foliar pesticide sprays before 10:00 AM tomorrow",
            plan_generated=False,
            plan_id=None
        )
    ]
    db.add_all(risks)

    # 7. Advisories
    advisories = [
        AIAdvisory(
            id="adv-01",
            farm_id="farm-greenvalley-01",
            title="Urgent Drip Irrigation for Cotton Field A",
            title_gu="કપાસ પ્લોટ A માં તાત્કાલિક ડ્રિપ પિયત આપવું",
            title_hi="कपास खेत A में तुरंत ड्रिप सिंचाई करें",
            field="Field A (Cotton)",
            priority="High",
            confidence_score=91,
            status="Pending Approval",
            timestamp="10:15 AM Today",
            orchestrator_summary="Water stress detected in flowering crop stage. AI recommends executing irrigation today between 6:00 PM and 8:00 PM.",
            explainability={
                "factors": [
                    {"name": "Current Root Moisture", "value": "31.4%", "impact": "Severe Deficit", "threshold": "Target 45%"},
                    {"name": "Rainfall Probability 24h", "value": "12%", "impact": "No Natural Rain Expected", "threshold": "< 30%"},
                    {"name": "Daytime Soil Temp", "value": "27.8°C", "impact": "High Transpiration Loss", "threshold": "Normal < 30°C"},
                    {"name": "Phenological Crop Stage", "value": "Flowering & Boll", "impact": "Critical Yield Sensitivity", "threshold": "Peak Water Need"}
                ],
                "whyText": "The Orchestrator Agent combined the Soil Agent's telemetry (31.4% moisture) with the Weather Agent's 24-hr rain prediction (only 12% probability). If irrigation is delayed past 24 hours, boll shedding risk will rise by 18%. Executing between 6:00 PM - 8:00 PM minimizes daytime evaporative loss by 28%."
            },
            action_details={
                "action": "Drip Irrigation",
                "volume": "2,500 Liters",
                "duration": "35 Minutes",
                "zone": "Field A - Zone 2 Solenoid",
                "costEstimate": "₹45 (Electricity)",
                "waterSource": "North Tube Well"
            }
        ),
        AIAdvisory(
            id="adv-02",
            farm_id="farm-greenvalley-01",
            title="Phosphorus Nutrient Top-Dressing for Field B",
            title_gu="ખેતર B માં ફોસ્ફરસ ખાતર આપવું",
            title_hi="खेत B में फास्फोरस उर्वरक डालें",
            field="Field B (Wheat)",
            priority="Medium",
            confidence_score=86,
            status="Approved",
            timestamp="09:30 AM Today",
            orchestrator_summary="Soil testing indicates available P at 14 mg/kg. Apply water-soluble DAP during tomorrow morning's fertigation.",
            explainability={
                "factors": [
                    {"name": "Available Phosphorus (P)", "value": "14 mg/kg", "impact": "Deficient", "threshold": "Optimal > 22 mg/kg"},
                    {"name": "Nitrogen & Potassium", "value": "Normal", "impact": "Balanced", "threshold": "No Intervention"},
                    {"name": "Wheat Tillering State", "value": "Active", "impact": "Root elongation dependent on P", "threshold": "Day 25-45"}
                ],
                "whyText": "Soil Agent detected that Phosphorus fell below the threshold due to rapid vegetative uptake during wheat tillering. Applying now ensures root vigor before stem elongation begins."
            },
            action_details={
                "action": "Fertigation (DAP / 12:61:00)",
                "volume": "15 kg Dissolved",
                "duration": "20 Minutes",
                "zone": "Field B Fertigation Venturi",
                "costEstimate": "₹420",
                "waterSource": "Drip Tank"
            }
        )
    ]
    db.add_all(advisories)

    # 8. Action Plans
    plans = [
        ActionPlan(
            id="PLAN-1024",
            farm_id="farm-greenvalley-01",
            title="Precision Water Stress Alleviation",
            target_field="Field A (Cotton - 5.2 Acres)",
            action_type="Automated Drip Irrigation",
            scheduled_time="Today • 18:00 - 18:35 IST",
            status="Approved",
            priority="High",
            estimated_cost=45.0,
            water_volume="2,500 L",
            constraints={
                "costBudget": "₹150 Max (Est: ₹45)",
                "weatherWindow": "Safe (Rain prob 12%, Wind 14 km/h)",
                "waterAvailability": "Tube Well Level: High (88%)",
                "safetyProtocols": "Electrical grounding checked, line pressure 1.8 bar"
            },
            hardware_target="Solenoid Valve SV-01 (Field A)",
            assigned_to="Automated IoT Valve + Kishanbhai"
        ),
        ActionPlan(
            id="PLAN-1025",
            farm_id="farm-greenvalley-01",
            title="Organic Pest Intervention Protocol",
            target_field="Field B (Wheat - 4.1 Acres)",
            action_type="Bio-Pesticide Spraying",
            scheduled_time="Tomorrow • 07:30 - 08:30 IST",
            status="Scheduled",
            priority="High",
            estimated_cost=180.0,
            water_volume="200 L Mix",
            constraints={
                "costBudget": "₹300 Max (Est: ₹180)",
                "weatherWindow": "Morning Window: Wind < 12 km/h, No rain",
                "waterAvailability": "Adequate Farm Tank storage",
                "safetyProtocols": "Protective mask and gloves required"
            },
            hardware_target="Battery Sprayer Kit #2",
            assigned_to="Field Worker: Ramesh Patel"
        )
    ]
    db.add_all(plans)

    # 9. Tasks
    tasks = [
        FarmTask(
            id="TSK-01",
            farm_id="farm-greenvalley-01",
            plan_id="PLAN-1024",
            title="Trigger Drip Irrigation in Field A",
            field="Field A",
            status="todo",
            priority="High",
            due_time="Today 18:00",
            assigned_to="IoT Valve (Auto) / Farmer",
            icon="Droplets",
            notes="Run for 35 mins. Auto-shutoff when soil moisture reaches 44%."
        ),
        FarmTask(
            id="TSK-02",
            farm_id="farm-greenvalley-01",
            plan_id="PLAN-1025",
            title="Prepare 1500 ppm Neem Bio-Solution",
            field="Field B",
            status="todo",
            priority="High",
            due_time="Tomorrow 07:00",
            assigned_to="Ramesh Patel",
            icon="Bug",
            notes="Mix 1 liter neem extract with 200 L clean water and 50g surfactant."
        ),
        FarmTask(
            id="TSK-03",
            farm_id="farm-greenvalley-01",
            plan_id="PLAN-1025",
            title="Inspect Field B East Border for Aphids",
            field="Field B",
            status="in-progress",
            priority="High",
            due_time="Today 16:30",
            assigned_to="Kishanbhai Patel",
            icon="Search",
            notes="Examine undersides of leaves on 20 random plants across plot."
        ),
        FarmTask(
            id="TSK-04",
            farm_id="farm-greenvalley-01",
            plan_id=None,
            title="Soil Moisture Sensor Calibration",
            field="Field C",
            status="completed",
            priority="Normal",
            due_time="Yesterday",
            assigned_to="AgriTech Field Support",
            icon="CheckCircle",
            notes="FDR probe zero-calibration verified against laboratory sample."
        )
    ]
    db.add_all(tasks)

    # 10. Audit Activity Logs
    logs = [
        ActivityLog(id="LOG-01", farm_id="farm-greenvalley-01", time="10:34 AM", agent="Farmer Interaction", event="Farmer approved Plan #1024 (Drip Irrigation)", severity="success"),
        ActivityLog(id="LOG-02", farm_id="farm-greenvalley-01", time="10:33 AM", agent="Master Orchestrator", event="Generated Action Plan #1024 with cost constraint ₹45", severity="info"),
        ActivityLog(id="LOG-03", farm_id="farm-greenvalley-01", time="10:32 AM", agent="Meteorological Agent", event="Scanned radar: rain probability 12% (safe for watering)", severity="info"),
        ActivityLog(id="LOG-04", farm_id="farm-greenvalley-01", time="10:30 AM", agent="Soil & Moisture Agent", event="Detected Root Deficit: Field A moisture 31.4% < threshold", severity="warning"),
        ActivityLog(id="LOG-05", farm_id="farm-greenvalley-01", time="09:15 AM", agent="Pest & Pathogen Agent", event="Spectral alert: leaf chlorosis patterns detected in Field B", severity="warning"),
        ActivityLog(id="LOG-06", farm_id="farm-greenvalley-01", time="07:00 AM", agent="Execution Agent", event="Automated daily sensor network ping completed: 4/4 nodes online", severity="success")
    ]
    db.add_all(logs)

    # 11. Escalation Tickets
    tickets = [
        ExpertReviewTicket(
            id="ESC-801",
            field="Field B (Wheat)",
            crop="Wheat",
            issue="Unusual Yellow Leaf Tip Necrosis with Low AI Confidence (58%)",
            ai_confidence=58,
            reason="Micro-image glare and overlapping fungal vs micronutrient symptoms",
            assigned_agronomist="Dr. Arvind Dave (Senior Agronomist, JAU Junagadh)",
            status="Review Pending",
            submitted_at="Today 08:30 AM",
            telemetry_snapshot={"moisture": "48%", "soilPH": "7.2", "nitrogen": "Normal", "phosphorus": "Low 14 mg/kg"},
            agronomist_notes="Scheduled video scouting call with Kishanbhai at 14:00 hrs. Suspect Zinc/Phosphorus interaction."
        )
    ]
    db.add_all(tickets)

    await db.commit()
    logger.info("GreenValley Farm seed data initialized successfully!")
