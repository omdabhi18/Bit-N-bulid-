"""
Seed 24 standardized agricultural crops into KrishiNetra platform database.
Supports English & Gujarati naming, category classification, scientific names,
and AI disease model capability flags.
Idempotent: updates existing records without creating duplicates or breaking field links.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime, timezone

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from Database.connection import AsyncSessionLocal, async_engine, Base
from Database.models.crop import Crop
from sqlalchemy.future import select


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("krishinetra.crop_seed")

CROP_CATALOG = [
    {
        "id": "cotton",
        "name": "Cotton",
        "name_gujarati": "કપાસ",
        "category": "Cash Crop",
        "scientific_name": "Gossypium hirsutum",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "BT Cotton RCH-2 / G.Cot.Hy-8",
        "current_stage": "Flowering & Boll Formation",
    },
    {
        "id": "wheat",
        "name": "Wheat",
        "name_gujarati": "ઘઉં",
        "category": "Cereal",
        "scientific_name": "Triticum aestivum",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "GW-496 / Sharbati",
        "current_stage": "Tillering (કૂટ અવસ્થા)",
    },
    {
        "id": "tomato",
        "name": "Tomato",
        "name_gujarati": "ટામેટા",
        "category": "Vegetable",
        "scientific_name": "Solanum lycopersicum",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "Abhinav / US-440",
        "current_stage": "Fruiting & Ripening",
    },
    {
        "id": "groundnut",
        "name": "Groundnut",
        "name_gujarati": "મગફળી",
        "category": "Oilseed",
        "scientific_name": "Arachis hypogaea",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "GG-20 / GJG-32",
        "current_stage": "Pod Development (સૂયા બેસવાની અવસ્થા)",
    },
    {
        "id": "rice",
        "name": "Rice",
        "name_gujarati": "ડાંગર",
        "category": "Cereal",
        "scientific_name": "Oryza sativa",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "Gurjari / GR-11",
        "current_stage": "Tillering / Panicle Initiation",
    },
    {
        "id": "maize",
        "name": "Maize",
        "name_gujarati": "મકાઈ",
        "category": "Cereal",
        "scientific_name": "Zea mays",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "African Tall / Sweet Corn",
        "current_stage": "Tasseling & Silking",
    },
    {
        "id": "bajra",
        "name": "Bajra",
        "name_gujarati": "બાજરી",
        "category": "Millet",
        "scientific_name": "Pennisetum glaucum",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "GHB-558",
        "current_stage": "Grain Formation",
    },
    {
        "id": "jowar",
        "name": "Jowar",
        "name_gujarati": "જુવાર",
        "category": "Millet",
        "scientific_name": "Sorghum bicolor",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "Gundari / CSV-15",
        "current_stage": "Vegetative",
    },
    {
        "id": "onion",
        "name": "Onion",
        "name_gujarati": "ડુંગળી",
        "category": "Vegetable",
        "scientific_name": "Allium cepa",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "Pilipatti / Nashik Red",
        "current_stage": "Bulb Development",
    },
    {
        "id": "potato",
        "name": "Potato",
        "name_gujarati": "બટાકા",
        "category": "Vegetable",
        "scientific_name": "Solanum tuberosum",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "Kufri Badshah / Pukhraj",
        "current_stage": "Tuber Initiation",
    },
    {
        "id": "chilli",
        "name": "Chilli",
        "name_gujarati": "મરચું",
        "category": "Vegetable / Spice",
        "scientific_name": "Capsicum annuum",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "Resham Patti / G-4",
        "current_stage": "Flowering & Fruit Setting",
    },
    {
        "id": "brinjal",
        "name": "Brinjal",
        "name_gujarati": "રીંગણ",
        "category": "Vegetable",
        "scientific_name": "Solanum melongena",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "Ravaiya / Doli-5",
        "current_stage": "Vegetative",
    },
    {
        "id": "okra",
        "name": "Okra",
        "name_gujarati": "ભીંડા",
        "category": "Vegetable",
        "scientific_name": "Abelmoschus esculentus",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "Gujarat Okra-3 / Radhika",
        "current_stage": "Harvesting / Fruiting",
    },
    {
        "id": "cabbage",
        "name": "Cabbage",
        "name_gujarati": "કોબી",
        "category": "Vegetable",
        "scientific_name": "Brassica oleracea var. capitata",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "Golden Acre",
        "current_stage": "Head Formation",
    },
    {
        "id": "cauliflower",
        "name": "Cauliflower",
        "name_gujarati": "ફૂલકોબી",
        "category": "Vegetable",
        "scientific_name": "Brassica oleracea var. botrytis",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "Pusa Deepali / Snowball",
        "current_stage": "Curd Development",
    },
    {
        "id": "soybean",
        "name": "Soybean",
        "name_gujarati": "સોયાબીન",
        "category": "Oilseed / Legume",
        "scientific_name": "Glycine max",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "JS-335 / NRC-37",
        "current_stage": "Pod Filling",
    },
    {
        "id": "sugarcane",
        "name": "Sugarcane",
        "name_gujarati": "શેરડી",
        "category": "Cash Crop",
        "scientific_name": "Saccharum officinarum",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "Co-86032",
        "current_stage": "Grand Growth",
    },
    {
        "id": "chickpea",
        "name": "Chickpea",
        "name_gujarati": "ચણા",
        "category": "Pulse",
        "scientific_name": "Cicer arietinum",
        "disease_ai_supported": True,
        "is_active": True,
        "variety": "Gujarat Gram-1 / Chana Dahod Yellow",
        "current_stage": "Pod Development",
    },
    {
        "id": "pigeon_pea",
        "name": "Pigeon Pea",
        "name_gujarati": "તુવેર",
        "category": "Pulse",
        "scientific_name": "Cajanus cajan",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "Vaishali / BDN-2",
        "current_stage": "Flowering",
    },
    {
        "id": "sesame",
        "name": "Sesame",
        "name_gujarati": "તલ",
        "category": "Oilseed",
        "scientific_name": "Sesamum indicum",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "Gujarat Til-2",
        "current_stage": "Capsule Formation",
    },
    {
        "id": "mustard",
        "name": "Mustard",
        "name_gujarati": "સરસવ",
        "category": "Oilseed",
        "scientific_name": "Brassica juncea",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "Gujarat Mustard-3 / Pusa Bold",
        "current_stage": "Siliqua Formation",
    },
    {
        "id": "castor",
        "name": "Castor",
        "name_gujarati": "એરંડા",
        "category": "Oilseed",
        "scientific_name": "Ricinus communis",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "GCH-7",
        "current_stage": "Primary Spike Maturity",
    },
    {
        "id": "green_gram",
        "name": "Green Gram",
        "name_gujarati": "મગ",
        "category": "Pulse",
        "scientific_name": "Vigna radiata",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "GM-4",
        "current_stage": "Podding",
    },
    {
        "id": "black_gram",
        "name": "Black Gram",
        "name_gujarati": "અડદ",
        "category": "Pulse",
        "scientific_name": "Vigna mungo",
        "disease_ai_supported": False,
        "is_active": True,
        "variety": "T-9 / GU-1",
        "current_stage": "Vegetative & Flowering",
    },
]


async def seed_crop_catalog():
    logger.info("Connecting to database and ensuring tables exist...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    async with AsyncSessionLocal() as session:
        logger.info("Seeding 24 standardized agricultural crops...")
        upserted = 0
        for item in CROP_CATALOG:
            res = await session.execute(select(Crop).where(Crop.id == item["id"]))
            existing = res.scalars().first()
            if existing:
                # Update catalog attributes while preserving existing farm/field linkages
                existing.name = item["name"]
                existing.name_gujarati = item["name_gujarati"]
                existing.crop_name = f"{item['name']} ({item['name_gujarati']})"
                existing.category = item["category"]
                existing.scientific_name = item["scientific_name"]
                existing.disease_ai_supported = item["disease_ai_supported"]
                existing.is_active = item["is_active"]
                existing.updated_at = datetime.now(timezone.utc)
            else:
                crop = Crop(
                    id=item["id"],
                    name=item["name"],
                    crop_name=f"{item['name']} ({item['name_gujarati']})",
                    name_gujarati=item["name_gujarati"],
                    category=item["category"],
                    scientific_name=item["scientific_name"],
                    disease_ai_supported=item["disease_ai_supported"],
                    is_active=item["is_active"],
                    variety=item.get("variety", "Standard Variety"),
                    current_stage=item.get("current_stage", "Vegetative"),
                    stage=item.get("current_stage", "Vegetative"),
                    area=5.0,
                    field_name="Catalog Sample",
                )
                session.add(crop)
            upserted += 1

        await session.commit()
        logger.info(f"Successfully seeded/updated {upserted} crops in the database!")


if __name__ == "__main__":
    asyncio.run(seed_crop_catalog())
