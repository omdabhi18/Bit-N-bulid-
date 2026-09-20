// Comprehensive realistic farm data modeled after Indian Precision Agriculture Systems

export const initialFarmProfile = {
  farmerName: "Kishanbhai Patel",
  farmName: "GreenValley Smart Farms",
  village: "Ribda",
  taluka: "Gondal",
  district: "Rajkot",
  state: "Gujarat",
  totalAreaAcre: 12.5,
  soilType: "Medium Black Clayey Loam (કાળી જમીન)",
  irrigationMethod: "Drip Automation + Tube Well",
  coordinates: { lat: 21.9619, lng: 70.7923 },
  crops: [
    { id: "cotton", name: "BT Cotton (કપાસ)", variety: "G.Cot.Hy-8", stage: "Flowering & Boll Formation", area: 5.2, field: "Field A", sowingDate: "2026-06-15" },
    { id: "wheat", name: "Sharbati Wheat (ઘઉં)", variety: "GW-496", stage: "Vegetative Tillering", area: 4.1, field: "Field B", sowingDate: "2026-11-10" },
    { id: "groundnut", name: "Groundnut (મગફળી)", variety: "GG-20", stage: "Pod Development", area: 3.2, field: "Field C", sowingDate: "2026-07-02" }
  ]
};

export const currentTelemetry = {
  farmHealthScore: 82, // percentage
  soilMoisture: 31.4, // percentage - below optimal 45%
  soilMoistureStatus: "Deficit (પાણીની જરૂર)",
  soilTemperature: 27.8, // Celsius
  soilPH: 6.8, // Optimal 6.5 - 7.5
  soilEC: 0.42, // dS/m
  nitrogenLevel: 82, // mg/kg (Normal)
  phosphorusLevel: 14, // mg/kg (LOW - below 20 mg/kg threshold)
  potassiumLevel: 185, // mg/kg (Good)
  airTemperature: 33.2, // Celsius
  airHumidity: 58, // %
  rainfallProb24h: 12, // %
  windSpeed: 14, // km/h
  solarRadiation: 820, // W/m2
  dripValveA: "Closed",
  dripValveB: "Standby",
  dripValveC: "Closed"
};

export const fieldsData = [
  {
    id: "field-a",
    name: "Field A - South Valley",
    crop: "BT Cotton (કપાસ)",
    area: "5.2 Acres",
    stage: "Flowering (ફૂલ અવસ્થા)",
    healthScore: 78,
    soilMoisture: 31,
    status: "Warning",
    riskCategory: "Water Stress",
    pestRisk: "Low (15%)",
    soilPH: 6.8,
    nitrogen: "Normal",
    phosphorus: "Optimal",
    potassium: "High",
    sensorNode: "SN-Cotton-01",
    sensorStatus: "Online",
    coordinates: [
      { lat: 21.9635, lng: 70.7910 },
      { lat: 21.9645, lng: 70.7938 },
      { lat: 21.9615, lng: 70.7945 },
      { lat: 21.9605, lng: 70.7915 }
    ],
    color: "#eab308", // warning yellow
    dripStatus: "Ready",
    recommendation: "Irrigation required within 6 hours (2,500 L)"
  },
  {
    id: "field-b",
    name: "Field B - North Ridge",
    crop: "Sharbati Wheat (ઘઉં)",
    area: "4.1 Acres",
    stage: "Tillering (કૂટ અવસ્થા)",
    healthScore: 71,
    soilMoisture: 48,
    status: "Critical",
    riskCategory: "Pest Risk & Phosphorus Deficiency",
    pestRisk: "High (78%) - Pink Bollworm / Aphid alert",
    soilPH: 7.2,
    nitrogen: "Optimal",
    phosphorus: "Low ⚠️ (14 mg/kg)",
    potassium: "Normal",
    sensorNode: "SN-Wheat-02",
    sensorStatus: "Online",
    coordinates: [
      { lat: 21.9650, lng: 70.7942 },
      { lat: 21.9670, lng: 70.7968 },
      { lat: 21.9642, lng: 70.7982 },
      { lat: 21.9628, lng: 70.7950 }
    ],
    color: "#ef4444", // critical red
    dripStatus: "Standby",
    recommendation: "Pest inspection and DAP fertilizer soil dressing required"
  },
  {
    id: "field-c",
    name: "Field C - East Plot",
    crop: "Groundnut (મગફળી)",
    area: "3.2 Acres",
    stage: "Pod Development (સૂયા બેસવાની અવસ્થા)",
    healthScore: 92,
    soilMoisture: 52,
    status: "Healthy",
    riskCategory: "Optimal Conditions",
    pestRisk: "None (8%)",
    soilPH: 6.9,
    nitrogen: "Good",
    phosphorus: "Optimal",
    potassium: "Optimal",
    sensorNode: "SN-Gnut-03",
    sensorStatus: "Online",
    coordinates: [
      { lat: 21.9600, lng: 70.7890 },
      { lat: 21.9620, lng: 70.7905 },
      { lat: 21.9595, lng: 70.7930 },
      { lat: 21.9580, lng: 70.7900 }
    ],
    color: "#22c55e", // healthy green
    dripStatus: "Optimal",
    recommendation: "Conditions ideal. Next scheduled scouting in 3 days"
  }
];

export const telemetryTimeSeries = [
  { time: "00:00", moisture: 38, temp: 23, humidity: 75, ec: 0.40 },
  { time: "03:00", moisture: 37, temp: 22, humidity: 79, ec: 0.40 },
  { time: "06:00", moisture: 36, temp: 24, humidity: 82, ec: 0.41 },
  { time: "09:00", moisture: 34, temp: 28, humidity: 68, ec: 0.41 },
  { time: "12:00", moisture: 33, temp: 32, humidity: 55, ec: 0.42 },
  { time: "15:00", moisture: 31, temp: 34, humidity: 50, ec: 0.42 },
  { time: "18:00", moisture: 31, temp: 30, humidity: 58, ec: 0.42 },
  { time: "21:00", moisture: 30, temp: 26, humidity: 65, ec: 0.41 }
];

export const npkRadarData = [
  { nutrient: "Nitrogen (N)", actual: 82, optimal: 75, fullMark: 100 },
  { nutrient: "Phosphorus (P)", actual: 35, optimal: 70, fullMark: 100 },
  { nutrient: "Potassium (K)", actual: 88, optimal: 80, fullMark: 100 },
  { nutrient: "Organic Carbon", actual: 65, optimal: 70, fullMark: 100 },
  { nutrient: "Zinc (Zn)", actual: 70, optimal: 65, fullMark: 100 },
  { nutrient: "Boron (B)", actual: 60, optimal: 60, fullMark: 100 }
];

export const hardwareSensors = [
  { id: "SN-Cotton-01", name: "Soil & Microclimate Node A", field: "Field A", battery: 94, signal: "Excellent (4G IoT)", status: "Online", lastSync: "1 minute ago", type: "FDR Moisture + NPK Probes" },
  { id: "SN-Wheat-02", name: "Soil & Leaf Sensor Node B", field: "Field B", battery: 88, signal: "Good (LoRaWAN)", status: "Online", lastSync: "3 minutes ago", type: "Soil Moisture + Multispectral Optical" },
  { id: "SN-Gnut-03", name: "Smart Drip Controller C", field: "Field C", battery: 100, signal: "Solar Mains (WiFi)", status: "Online", lastSync: "Just now", type: "Solenoid Valve + EC Sensor" },
  { id: "SN-Weather-04", name: "Micro Weather Station", field: "Central Farm", battery: 98, signal: "Satellite IoT", status: "Online", lastSync: "2 minutes ago", type: "Anemometer + Pyranometer + Rain Gauge" }
];

export const detectedRisks = [
  {
    id: "risk-01",
    category: "Water Stress (પાણીની અછત)",
    icon: "Droplets",
    severity: "High",
    field: "Field A (Cotton)",
    probability: 88,
    indicators: [
      "Soil moisture dropped to 31% (critical wilting point: 28%)",
      "Evapotranspiration rate elevated at 5.8 mm/day due to 34°C peak temp",
      "Flowering stage requires consistent 40-50% root-zone moisture"
    ],
    recommendedAction: "Targeted drip irrigation of 2,500 L at 18:00 hrs",
    planGenerated: true,
    planId: "PLAN-1024"
  },
  {
    id: "risk-02",
    category: "Pest Risk (જીવાત ઉપદ્રવ)",
    icon: "Bug",
    severity: "Critical",
    field: "Field B (Wheat)",
    probability: 78,
    indicators: [
      "Nocturnal humidity > 78% combined with 22°C ambient favors aphid multiplication",
      "Spectral imagery highlights leaf chlorosis in eastern sub-zone",
      "Regional APMC pest advisory reports early bollworm emergence"
    ],
    recommendedAction: "Physical scouting + Organic Neem-oil formulation spray (1500 ppm)",
    planGenerated: true,
    planId: "PLAN-1025"
  },
  {
    id: "risk-03",
    category: "Nutrient Deficiency (પોષક તત્વોની ખામી)",
    icon: "Sprout",
    severity: "Medium",
    field: "Field B (Wheat)",
    probability: 69,
    indicators: [
      "Phosphorus detected at 14 mg/kg (benchmark minimum is 22 mg/kg)",
      "Slow tillering root extension observed",
      "Soil EC remains within safe osmotic range (0.42 dS/m)"
    ],
    recommendedAction: "Apply 25 kg DAP or rock phosphate during next fertigation cycle",
    planGenerated: false
  },
  {
    id: "risk-04",
    category: "Weather Risk (હવામાન અસર)",
    icon: "CloudRain",
    severity: "Medium",
    field: "All Fields",
    probability: 62,
    indicators: [
      "Sudden gusty winds (up to 32 km/h) forecasted for tomorrow afternoon",
      "Scattered drizzle probability 35% on Day 3",
      "Avoid foliar spraying during high wind velocity to prevent drift loss"
    ],
    recommendedAction: "Complete any foliar pesticide sprays before 10:00 AM tomorrow",
    planGenerated: false
  },
  {
    id: "risk-05",
    category: "Market Timing Risk (બજાર ભાવ)",
    icon: "TrendingUp",
    severity: "Low",
    field: "Cotton Harvest Batch",
    probability: 54,
    indicators: [
      "Rajkot APMC cotton rates rose 4.2% this week to ₹7,380/quintal",
      "National cotton arrivals expected to peak in 10 days, potentially softening spot prices",
      "Optimal selling window predicted within the next 4 to 6 days"
    ],
    recommendedAction: "Book APMC slot for 60% of stored cotton stock at current high rates",
    planGenerated: false
  }
];

export const aiAdvisories = [
  {
    id: "adv-01",
    title: "Urgent Drip Irrigation for Cotton Field A",
    titleGu: "કપાસ પ્લોટ A માં તાત્કાલિક ડ્રિપ પિયત આપવું",
    titleHi: "कपास खेत A में तुरंत ड्रिप सिंचाई करें",
    field: "Field A (Cotton)",
    priority: "High",
    confidenceScore: 91,
    status: "Pending Approval",
    timestamp: "10:15 AM Today",
    orchestratorSummary: "Water stress detected in flowering crop stage. AI recommends executing irrigation today between 6:00 PM and 8:00 PM.",
    explainability: {
      factors: [
        { name: "Current Root Moisture", value: "31.4%", impact: "Severe Deficit", threshold: "Target 45%" },
        { name: "Rainfall Probability 24h", value: "12%", impact: "No Natural Rain Expected", threshold: "< 30%" },
        { name: "Daytime Soil Temp", value: "27.8°C", impact: "High Transpiration Loss", threshold: "Normal < 30°C" },
        { name: "Phenological Crop Stage", value: "Flowering & Boll", impact: "Critical Yield Sensitivity", threshold: "Peak Water Need" }
      ],
      whyText: "The Orchestrator Agent combined the Soil Agent's telemetry (31.4% moisture) with the Weather Agent's 24-hr rain prediction (only 12% probability). If irrigation is delayed past 24 hours, boll shedding risk will rise by 18%. Executing between 6:00 PM - 8:00 PM minimizes daytime evaporative loss by 28%."
    },
    actionDetails: {
      action: "Drip Irrigation",
      volume: "2,500 Liters",
      duration: "35 Minutes",
      zone: "Field A - Zone 2 Solenoid",
      costEstimate: "₹45 (Electricity)",
      waterSource: "North Tube Well"
    }
  },
  {
    id: "adv-02",
    title: "Phosphorus Nutrient Top-Dressing for Field B",
    titleGu: "ખેતર B માં ફોસ્ફરસ ખાતર આપવું",
    titleHi: "खेत B में फास्फोरस उर्वरक डालें",
    field: "Field B (Wheat)",
    priority: "Medium",
    confidenceScore: 86,
    status: "Approved",
    timestamp: "09:30 AM Today",
    orchestratorSummary: "Soil testing indicates available P at 14 mg/kg. Apply water-soluble DAP during tomorrow morning's fertigation.",
    explainability: {
      factors: [
        { name: "Available Phosphorus (P)", value: "14 mg/kg", impact: "Deficient", threshold: "Optimal > 22 mg/kg" },
        { name: "Nitrogen & Potassium", value: "Normal", impact: "Balanced", threshold: "No Intervention" },
        { name: "Wheat Tillering State", value: "Active", impact: "Root elongation dependent on P", threshold: "Day 25-45" }
      ],
      whyText: "Soil Agent detected that Phosphorus fell below the threshold due to rapid vegetative uptake during wheat tillering. Applying now ensures root vigor before stem elongation begins."
    },
    actionDetails: {
      action: "Fertigation (DAP / 12:61:00)",
      volume: "15 kg Dissolved",
      duration: "20 Minutes",
      zone: "Field B Fertigation Venturi",
      costEstimate: "₹420",
      waterSource: "Drip Tank"
    }
  },
  {
    id: "adv-03",
    title: "Pest Scouting & Preventive Bio-Spray",
    titleGu: "ગુલાબી ઈયળ તપાસ અને જૈવિક લીમડાના તેલનો છંટકાવ",
    titleHi: "कीट निरीक्षण और जैविक नीम तेल छिड़काव",
    field: "Field B (Wheat & Border Cotton)",
    priority: "High",
    confidenceScore: 78,
    status: "Pending Approval",
    timestamp: "08:45 AM Today",
    orchestratorSummary: "Pest Agent alerted high aphid and early bollworm probability following sustained nighttime humidity > 75%.",
    explainability: {
      factors: [
        { name: "Relative Night Humidity", value: "79%", impact: "Favorable for Micro-pests", threshold: "> 70%" },
        { name: "Neighboring Field Alert", value: "Reported in 2 km", impact: "Vector Migration Risk", threshold: "Active Alert" },
        { name: "Leaf Image Diagnosis", value: "Minor Yellow Stippling", impact: "Early Stage", threshold: "< 5% Leaf Area" }
      ],
      whyText: "Pest Agent and Crop Health Agent cross-correlated regional APMC pest bulletin with your localized micrometeorology. Bio-spray prevents chemical pesticide residue and safeguards natural pollinators."
    },
    actionDetails: {
      action: "Neem Oil Spray (1500 ppm)",
      volume: "200 L Solution",
      duration: "45 Minutes",
      zone: "Knapsack Sprayer - Field B",
      costEstimate: "₹180",
      waterSource: "Farm Tank"
    }
  }
];

export const initialActionPlans = [
  {
    id: "PLAN-1024",
    title: "Precision Water Stress Alleviation",
    targetField: "Field A (Cotton - 5.2 Acres)",
    actionType: "Automated Drip Irrigation",
    scheduledTime: "Today • 18:00 - 18:35 IST",
    status: "Approved", // Draft, Approved, Scheduled, In Progress, Completed
    priority: "High",
    estimatedCost: 45,
    waterVolume: "2,500 L",
    constraints: {
      costBudget: "₹150 Max (Est: ₹45)",
      weatherWindow: "Safe (Rain prob 12%, Wind 14 km/h)",
      waterAvailability: "Tube Well Level: High (88%)",
      safetyProtocols: "Electrical grounding checked, line pressure 1.8 bar"
    },
    hardwareTarget: "Solenoid Valve SV-01 (Field A)",
    assignedTo: "Automated IoT Valve + Kisanbhai"
  },
  {
    id: "PLAN-1025",
    title: "Organic Pest Intervention Protocol",
    targetField: "Field B (Wheat - 4.1 Acres)",
    actionType: "Bio-Pesticide Spraying",
    scheduledTime: "Tomorrow • 07:30 - 08:30 IST",
    status: "Scheduled",
    priority: "High",
    estimatedCost: 180,
    waterVolume: "200 L Mix",
    constraints: {
      costBudget: "₹300 Max (Est: ₹180)",
      weatherWindow: "Morning Window: Wind < 12 km/h, No rain",
      waterAvailability: "Adequate Farm Tank storage",
      safetyProtocols: "Protective mask and gloves required"
    },
    hardwareTarget: "Battery Sprayer Kit #2",
    assignedTo: "Field Worker: Ramesh Patel"
  },
  {
    id: "PLAN-1026",
    title: "Phosphorus Fertigation Cycle",
    targetField: "Field B (Wheat)",
    actionType: "Soil Nutrient Enrichment",
    scheduledTime: "Day After Tomorrow • 09:00 IST",
    status: "Draft",
    priority: "Medium",
    estimatedCost: 420,
    waterVolume: "1,200 L",
    constraints: {
      costBudget: "₹500 Max (Est: ₹420)",
      weatherWindow: "Clear sunshine required for root uptake",
      waterAvailability: "Good",
      safetyProtocols: "Pre-dissolve DAP 2 hours in advance"
    },
    hardwareTarget: "Venturi Injector Valve #2",
    assignedTo: "Kishanbhai Patel"
  }
];

export const initialTasks = [
  {
    id: "TSK-01",
    title: "Trigger Drip Irrigation in Field A",
    field: "Field A",
    planId: "PLAN-1024",
    status: "todo", // todo, in-progress, completed
    priority: "High",
    dueTime: "Today 18:00",
    assignedTo: "IoT Valve (Auto) / Farmer",
    icon: "Droplets",
    notes: "Run for 35 mins. Auto-shutoff when soil moisture reaches 44%."
  },
  {
    id: "TSK-02",
    title: "Prepare 1500 ppm Neem Bio-Solution",
    field: "Field B",
    planId: "PLAN-1025",
    status: "todo",
    priority: "High",
    dueTime: "Tomorrow 07:00",
    assignedTo: "Ramesh Patel",
    icon: "Bug",
    notes: "Mix 1 liter neem extract with 200 L clean water and 50g surfactant."
  },
  {
    id: "TSK-03",
    title: "Inspect Field B East Border for Aphids",
    field: "Field B",
    planId: "PLAN-1025",
    status: "in-progress",
    priority: "High",
    dueTime: "Today 16:30",
    assignedTo: "Kishanbhai Patel",
    icon: "Search",
    notes: "Examine undersides of leaves on 20 random plants across plot."
  },
  {
    id: "TSK-04",
    title: "Soil Moisture Sensor Calibration",
    field: "Field C",
    planId: null,
    status: "completed",
    priority: "Normal",
    dueTime: "Yesterday",
    assignedTo: "AgriTech Field Support",
    icon: "CheckCircle",
    notes: "FDR probe zero-calibration verified against laboratory sample."
  },
  {
    id: "TSK-05",
    title: "Clean Drip Disc Filters",
    field: "Central Pump",
    planId: null,
    status: "completed",
    priority: "Normal",
    dueTime: "2 Days Ago",
    assignedTo: "Kishanbhai Patel",
    icon: "Wrench",
    notes: "Flushed sand and algae backwash. Pressure restored to 2.2 bar."
  }
];

export const aiAgents = [
  {
    id: "orchestrator",
    name: "Master Orchestrator Agent",
    role: "System Coordinator & Decision Synthesizer",
    status: "Active",
    confidence: 96,
    lastRun: "1 min ago",
    currentTask: "Synthesizing soil deficit & weather forecast into action schedule",
    inputs: ["Soil Agent telemetry", "Weather API 7-day", "Crop phenology state"],
    outputs: ["Plan #1024 Generated", "Advisory #01 Released", "Risk Matrix Updated"],
    icon: "Brain"
  },
  {
    id: "soil",
    name: "Soil & Moisture Agent",
    role: "Root Zone Telemetry & Nutrient Modeler",
    status: "Active",
    confidence: 94,
    lastRun: "3 mins ago",
    currentTask: "Continuously calculating soil water depletion in Field A root zone",
    inputs: ["FDR moisture probes", "Soil temp 27.8°C", "pH 6.8", "EC 0.42"],
    outputs: ["Water Deficit Alert (31.4%)", "Phosphorus Low Flag (14 mg/kg)"],
    icon: "Layers"
  },
  {
    id: "weather",
    name: "Meteorological Agent",
    role: "Hyperlocal Weather & Microclimate Forecast",
    status: "Active",
    confidence: 92,
    lastRun: "4 mins ago",
    currentTask: "Scanning Doppler radar and IMD satellite layers for rain chances",
    inputs: ["IMD regional grid", "Local barometric pressure", "Wind velocity 14 km/h"],
    outputs: ["Rainfall 24h: 12%", "Safe Spray Window: Tomorrow 07:00-10:00"],
    icon: "CloudSun"
  },
  {
    id: "crop",
    name: "Crop Phenology & Health Agent",
    role: "Growth Stage & Yield Optimization",
    status: "Active",
    confidence: 89,
    lastRun: "7 mins ago",
    currentTask: "Estimating cotton flowering water sensitivity index",
    inputs: ["Sowing date June 15", "GDD (Growing Degree Days): 1120", "NDVI 0.72"],
    outputs: ["Flowering stage confirmed", "Critical water stress vulnerability = High"],
    icon: "Sprout"
  },
  {
    id: "pest",
    name: "Pest & Pathogen Vision Agent",
    role: "Early Disease Warning & Bio-controls",
    status: "Active",
    confidence: 88,
    lastRun: "12 mins ago",
    currentTask: "Matching leaf chlorosis image patterns with regional pest outbreak",
    inputs: ["Thermal imaging", "Field B photo scans", "Nighttime humidity > 78%"],
    outputs: ["Aphid Risk = 78%", "Recommended Neem 1500ppm bio-spray"],
    icon: "Bug"
  },
  {
    id: "market",
    name: "APMC Mandi & Market Agent",
    role: "Price Arbitrage & Optimal Harvest Timing",
    status: "Active",
    confidence: 90,
    lastRun: "15 mins ago",
    currentTask: "Evaluating spot prices across Rajkot, Gondal, and Amreli mandis",
    inputs: ["Agmarknet API", "Commodity futures", "Local arrival volumes"],
    outputs: ["Cotton Rate ₹7,380 (+4.2%)", "Suggested Selling Window: 4-6 Days"],
    icon: "TrendingUp"
  },
  {
    id: "planner",
    name: "Constrained Action Planner",
    role: "Constraint Solver (Cost, Weather, Resources)",
    status: "Active",
    confidence: 93,
    lastRun: "1 min ago",
    currentTask: "Validating irrigation run time against electricity tariff & rain window",
    inputs: ["Advisory #01", "Max budget constraint ₹150", "Weather safe window"],
    outputs: ["Plan #1024 parameters locked (35 mins, ₹45, 18:00 IST)"],
    icon: "CalendarCheck"
  },
  {
    id: "execution",
    name: "Execution & Feedback Agent",
    role: "IoT Valve Triggers, Notifications & Escalation",
    status: "Active",
    confidence: 98,
    lastRun: "Just now",
    currentTask: "Monitoring farmer SMS/WhatsApp acknowledgment and valve heartbeat",
    inputs: ["Plan #1024 Approved status", "SV-01 valve ping", "SMS gateway"],
    outputs: ["Valve SV-01 armed for 18:00", "Push notification sent to farmer"],
    icon: "Cpu"
  }
];

export const cropDiseaseCatalog = [
  {
    id: "dis-01",
    crop: "Cotton (કપાસ)",
    diseaseName: "Cotton Leaf Curl Virus & Bacterial Blight",
    diseaseNameGu: "કપાસના પાન વળવાનો રોગ અને બેક્ટેરિયલ બ્લાઇટ",
    confidence: 88,
    severity: "High",
    image: "https://images.unsplash.com/photo-1599818490533-3d0d540df167?auto=format&fit=crop&w=800&q=80",
    symptoms: [
      "Upward curling and thickening of leaf veins",
      "Angular water-soaked spots transforming into reddish brown lesions",
      "Stunted vegetative terminal growth"
    ],
    recommendedRemedy: {
      organic: "Spray 5% Neem Seed Kernel Extract (NSKE) or Panchagavya (30 ml/L)",
      chemical: "Streptocycline (100 ppm) + Copper Oxychloride (2.5 g/L) during dry canopy hours",
      prevention: "Manage whitefly population early; avoid excessive late nitrogenous fertilizer"
    }
  },
  {
    id: "dis-02",
    crop: "Wheat (ઘઉં)",
    diseaseName: "Yellow / Stripe Rust (Puccinia striiformis)",
    diseaseNameGu: "ઘઉંનો પીળો ગેરુ રોગ",
    confidence: 92,
    severity: "Critical",
    image: "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=800&q=80",
    symptoms: [
      "Yellow to orange-colored powdery pustules arranged in parallel stripes",
      "Leaves turn chlorotic and dry prematurely",
      "Severe grain shriveling if untreated during flowering"
    ],
    recommendedRemedy: {
      organic: "Trichoderma viride bio-fungicide foliar application (5 g/L)",
      chemical: "Propiconazole 25% EC (1 ml/L water) or Tebuconazole",
      prevention: "Adopt rust-resistant varieties (GW-496 / HD-2967); avoid stagnant field water"
    }
  },
  {
    id: "dis-03",
    crop: "Tomato & Vegetables (ટામેટા)",
    diseaseName: "Early Blight (Alternaria solani)",
    diseaseNameGu: "ટામેટામાં આગોતરો સુકારો",
    confidence: 85,
    severity: "Medium",
    image: "https://images.unsplash.com/photo-1592417817098-8f3d6910985b?auto=format&fit=crop&w=800&q=80",
    symptoms: [
      "Concentric circular dark brown rings (target board pattern) on older leaves",
      "Yellow chlorotic halo surrounding lesions",
      "Lower canopy defoliation"
    ],
    recommendedRemedy: {
      organic: "Cow urine formulation (Gomutra 10%) + fermented sour buttermilk spray",
      chemical: "Mancozeb 75% WP (2 g/L) or Azoxystrobin (1 ml/L)",
      prevention: "Mulching to prevent soil splashing onto foliage; drip irrigation over sprinkler"
    }
  },
  {
    id: "dis-04",
    crop: "Groundnut (મગફળી)",
    diseaseName: "Tikka Leaf Spot (Cercospora arachidicola)",
    diseaseNameGu: "મગફળીમાં ટીક્કા (ટપકા)નો રોગ",
    confidence: 90,
    severity: "Medium",
    image: "https://images.unsplash.com/photo-1597916829826-02e5bb4a54e0?auto=format&fit=crop&w=800&q=80",
    symptoms: [
      "Dark brown circular spots with bright yellow borders on leaf surfaces",
      "Premature leaf shedding causing reduction in pod size",
      "Spread accelerated by warm humid periods"
    ],
    recommendedRemedy: {
      organic: "Pseudomonas fluorescens (10 g/L) bio-spray",
      chemical: "Carbendazim 12% + Mancozeb 63% WP (2 g/L)",
      prevention: "Crop rotation with non-host cereals; certified seed treatment"
    }
  }
];

export const weatherForecast = {
  current: {
    temp: 33,
    condition: "Mostly Sunny",
    humidity: 58,
    wind: "14 km/h SW",
    rainfallProb: 12,
    uvIndex: 8,
    dewPoint: 22,
    et0: "5.8 mm/day",
    advisory: "Favorable conditions for drip irrigation this evening. Wind speed safe for low-drift activities."
  },
  hourly: [
    { time: "12:00", temp: 33, rainProb: 10, humidity: 55 },
    { time: "14:00", temp: 34, rainProb: 12, humidity: 52 },
    { time: "16:00", temp: 32, rainProb: 15, humidity: 56 },
    { time: "18:00", temp: 30, rainProb: 12, humidity: 62 },
    { time: "20:00", temp: 27, rainProb: 10, humidity: 68 },
    { time: "22:00", temp: 25, rainProb: 8, humidity: 72 }
  ],
  daily: [
    { day: "Today", tempMax: 34, tempMin: 22, rainProb: 12, condition: "Sunny", sprayRating: "Good (After 17:00)" },
    { day: "Tomorrow", tempMax: 33, tempMin: 23, rainProb: 25, condition: "Partly Cloudy", sprayRating: "Morning Only (Wind alert)" },
    { day: "Day 3", tempMax: 31, tempMin: 21, rainProb: 45, condition: "Scattered Rain", sprayRating: "Poor (Rain risk)" },
    { day: "Day 4", tempMax: 30, tempMin: 20, rainProb: 30, condition: "Cloudy", sprayRating: "Moderate" },
    { day: "Day 5", tempMax: 32, tempMin: 21, rainProb: 15, condition: "Sunny", sprayRating: "Excellent" },
    { day: "Day 6", tempMax: 33, tempMin: 22, rainProb: 10, condition: "Clear Sky", sprayRating: "Excellent" },
    { day: "Day 7", tempMax: 34, tempMin: 23, rainProb: 8, condition: "Hot & Clear", sprayRating: "Good" }
  ]
};

export const marketCommodities = [
  {
    id: "comm-cotton",
    crop: "Shankar-6 Cotton (કપાસ)",
    unit: "₹ / Quintal (100 kg)",
    currentPrice: 7380,
    change7d: 4.2,
    trend: "up",
    mspPrice: 7122,
    aiRecommendation: "Favorable Selling Window. Prices at 4-week high due to export demand.",
    nearbyMarkets: [
      { name: "Rajkot APMC (રાજકોટ)", price: 7380, distance: "14 km", arrivals: "3,200 Qtl" },
      { name: "Gondal APMC (ગોંડલ)", price: 7420, distance: "22 km", arrivals: "4,100 Qtl" },
      { name: "Amreli APMC (અમરેલી)", price: 7290, distance: "58 km", arrivals: "2,800 Qtl" },
      { name: "Jasdan APMC (જસદણ)", price: 7310, distance: "45 km", arrivals: "1,900 Qtl" }
    ],
    priceHistory: [
      { day: "Mon", price: 7080 },
      { day: "Tue", price: 7150 },
      { day: "Wed", price: 7220 },
      { day: "Thu", price: 7310 },
      { day: "Fri", price: 7350 },
      { day: "Sat", price: 7380 },
      { day: "Today", price: 7380 }
    ]
  },
  {
    id: "comm-wheat",
    crop: "Lokwan / Sharbati Wheat (ઘઉં)",
    unit: "₹ / Quintal",
    currentPrice: 2850,
    change7d: 1.8,
    trend: "up",
    mspPrice: 2275,
    aiRecommendation: "Hold Inventory. Government procurement starting in 2 weeks expected to boost local mill demand.",
    nearbyMarkets: [
      { name: "Rajkot APMC", price: 2850, distance: "14 km", arrivals: "1,400 Qtl" },
      { name: "Gondal APMC", price: 2890, distance: "22 km", arrivals: "2,100 Qtl" },
      { name: "Unjha APMC", price: 2920, distance: "190 km", arrivals: "3,500 Qtl" }
    ],
    priceHistory: [
      { day: "Mon", price: 2790 },
      { day: "Tue", price: 2810 },
      { day: "Wed", price: 2820 },
      { day: "Thu", price: 2830 },
      { day: "Fri", price: 2845 },
      { day: "Sat", price: 2850 },
      { day: "Today", price: 2850 }
    ]
  },
  {
    id: "comm-groundnut",
    crop: "Groundnut GG-20 (મગફળી)",
    unit: "₹ / Quintal",
    currentPrice: 6520,
    change7d: -0.9,
    trend: "down",
    mspPrice: 6783,
    aiRecommendation: "Sell at MSP Center if open; otherwise store in warehouse until festive oil crushing peak.",
    nearbyMarkets: [
      { name: "Gondal APMC", price: 6580, distance: "22 km", arrivals: "5,400 Qtl" },
      { name: "Rajkot APMC", price: 6520, distance: "14 km", arrivals: "4,200 Qtl" },
      { name: "Junagadh APMC", price: 6490, distance: "95 km", arrivals: "3,100 Qtl" }
    ],
    priceHistory: [
      { day: "Mon", price: 6610 },
      { day: "Tue", price: 6590 },
      { day: "Wed", price: 6560 },
      { day: "Thu", price: 6540 },
      { day: "Fri", price: 6530 },
      { day: "Sat", price: 6520 },
      { day: "Today", price: 6520 }
    ]
  }
];

export const auditActivityLog = [
  { id: "LOG-01", time: "10:34 AM", agent: "Farmer Interaction", event: "Farmer approved Plan #1024 (Drip Irrigation)", severity: "success" },
  { id: "LOG-02", time: "10:33 AM", agent: "Master Orchestrator", event: "Generated Action Plan #1024 with cost constraint ₹45", severity: "info" },
  { id: "LOG-03", time: "10:32 AM", agent: "Meteorological Agent", event: "Scanned radar: rain probability 12% (safe for watering)", severity: "info" },
  { id: "LOG-04", time: "10:30 AM", agent: "Soil & Moisture Agent", event: "Detected Root Deficit: Field A moisture 31.4% < threshold", severity: "warning" },
  { id: "LOG-05", time: "09:15 AM", agent: "Pest & Pathogen Agent", event: "Spectral alert: leaf chlorosis patterns detected in Field B", severity: "warning" },
  { id: "LOG-06", time: "07:00 AM", agent: "Execution Agent", event: "Automated daily sensor network ping completed: 4/4 nodes online", severity: "success" }
];

export const escalationTickets = [
  {
    id: "ESC-801",
    field: "Field B (Wheat)",
    crop: "Wheat",
    issue: "Unusual Yellow Leaf Tip Necrosis with Low AI Confidence (58%)",
    aiConfidence: 58,
    reason: "Micro-image glare and overlapping fungal vs micronutrient symptoms",
    assignedAgronomist: "Dr. Arvind Dave (Senior Agronomist, JAU Junagadh)",
    status: "Review Pending",
    submittedAt: "Today 08:30 AM",
    telemetrySnapshot: { moisture: "48%", soilPH: "7.2", nitrogen: "Normal", phosphorus: "Low 14 mg/kg" },
    agronomistNotes: "Scheduled video scouting call with Kishanbhai at 14:00 hrs. Suspect Zinc/Phosphorus interaction."
  }
];
