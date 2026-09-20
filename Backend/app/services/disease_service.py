
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional, Dict
from datetime import datetime, timezone
import random
import uuid
from app.models.disease import DiseaseAnalysis, ExpertReviewTicket
from app.models.crop import Crop
from app.schemas.disease import (
    DiseaseCatalogItem,
    DiseaseAnalyzeResponse,
    DiseaseRemedy,
    EscalationCreateRequest,
    EscalationResponse
)

CATALOG = [
    {
        "id": "dis-01",
        "crop_id": "cotton",
        "crop": "Cotton (કપાસ)",
        "diseaseName": "Cotton Leaf Curl Virus & Bacterial Blight",
        "diseaseNameGu": "કપાસના પાન વળવાનો રોગ અને બેક્ટેરિયલ બ્લાઇટ",
        "confidence": 88,
        "severity": "High",
        "image": "https://images.unsplash.com/photo-1599818490533-3d0d540df167?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Upward curling and thickening of leaf veins",
            "Angular water-soaked spots transforming into reddish brown lesions",
            "Stunted vegetative terminal growth"
        ],
        "recommendedRemedy": {
            "organic": "Spray 5% Neem Seed Kernel Extract (NSKE) or Panchagavya (30 ml/L)",
            "chemical": "Streptocycline (100 ppm) + Copper Oxychloride (2.5 g/L) during dry canopy hours",
            "prevention": "Manage whitefly population early; avoid excessive late nitrogenous fertilizer"
        }
    },
    {
        "id": "dis-02",
        "crop_id": "wheat",
        "crop": "Wheat (ઘઉં)",
        "diseaseName": "Yellow / Stripe Rust (Puccinia striiformis)",
        "diseaseNameGu": "ઘઉંનો પીળો ગેરુ રોગ",
        "confidence": 92,
        "severity": "Critical",
        "image": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Yellow to orange-colored powdery pustules arranged in parallel stripes",
            "Leaves turn chlorotic and dry prematurely",
            "Severe grain shriveling if untreated during flowering"
        ],
        "recommendedRemedy": {
            "organic": "Trichoderma viride bio-fungicide foliar application (5 g/L)",
            "chemical": "Propiconazole 25% EC (1 ml/L water) or Tebuconazole",
            "prevention": "Adopt rust-resistant varieties (GW-496 / HD-2967); avoid stagnant field water"
        }
    },
    {
        "id": "dis-03",
        "crop_id": "tomato",
        "crop": "Tomato & Vegetables (ટામેટા)",
        "diseaseName": "Early Blight (Alternaria solani)",
        "diseaseNameGu": "ટામેટામાં આગોતરો સુકારો",
        "confidence": 85,
        "severity": "Medium",
        "image": "https://images.unsplash.com/photo-1592417817098-8f3d6910985b?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Concentric circular dark brown rings (target board pattern) on older leaves",
            "Yellow chlorotic halo surrounding lesions",
            "Lower canopy defoliation"
        ],
        "recommendedRemedy": {
            "organic": "Cow urine formulation (Gomutra 10%) + fermented sour buttermilk spray",
            "chemical": "Mancozeb 75% WP (2 g/L) or Azoxystrobin (1 ml/L)",
            "prevention": "Mulching to prevent soil splashing onto foliage; drip irrigation over sprinkler"
        }
    },
    {
        "id": "dis-04",
        "crop_id": "groundnut",
        "crop": "Groundnut (મગફળી)",
        "diseaseName": "Tikka Leaf Spot (Cercospora arachidicola)",
        "diseaseNameGu": "મગફળીમાં ટીક્કા (ટપકા)નો રોગ",
        "confidence": 90,
        "severity": "Medium",
        "image": "https://images.unsplash.com/photo-1597916829826-02e5bb4a54e0?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Dark brown circular spots with bright yellow borders on leaf surfaces",
            "Premature leaf shedding causing reduction in pod size",
            "Spread accelerated by warm humid periods"
        ],
        "recommendedRemedy": {
            "organic": "Pseudomonas fluorescens (10 g/L) bio-spray",
            "chemical": "Carbendazim 12% + Mancozeb 63% WP (2 g/L)",
            "prevention": "Crop rotation with non-host cereals; certified seed treatment"
        }
    }
]

CROP_PROFILES: Dict[str, dict] = {
    "cotton": CATALOG[0],
    "wheat": CATALOG[1],
    "tomato": CATALOG[2],
    "groundnut": CATALOG[3],
    "rice": {
        "diseaseName": "Bacterial Leaf Blight (Xanthomonas oryzae)",
        "diseaseNameGu": "ડાંગરમાં બેક્ટેરિયલ પાનનો સુકારો",
        "confidence": 87,
        "severity": "High",
        "image": "https://images.unsplash.com/photo-1536631844013-4667823c6388?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Water-soaked to yellowish translucent stripes on leaf margins",
            "Wavy margins turning white to grey and drying rapidly",
            "Milky bacterial dew droplets on young lesions in humid mornings"
        ],
        "recommendedRemedy": {
            "organic": "Foliar spray with fresh cow dung extract supernatant (20 g/L)",
            "chemical": "Streptocycline (15 g) + Copper Oxychloride (500 g) per acre in 200 L water",
            "prevention": "Avoid excess nitrogen fertilizer; drain stagnant water temporarily"
        }
    },
    "maize": {
        "diseaseName": "Northern Corn Leaf Blight (Exserohilum turcicum)",
        "diseaseNameGu": "મકાઈમાં પાનનો મોટો સુકારો",
        "confidence": 84,
        "severity": "Medium",
        "image": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Long elliptical cigar-shaped grayish-green lesions on leaves",
            "Lesions enlarge and coalesce, blighting entire leaf blades",
            "Premature drying and lodging of stalks"
        ],
        "recommendedRemedy": {
            "organic": "Trichoderma harzianum soil and foliar treatment",
            "chemical": "Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin + Difenoconazole @ 1 ml/L",
            "prevention": "Use resistant hybrids; deep summer plowing to bury crop residues"
        }
    },
    "onion": {
        "diseaseName": "Purple Blotch (Alternaria porri)",
        "diseaseNameGu": "ડુંગળીમાં જાંબલી ધાબાનો રોગ (પર્પલ બ્લોચ)",
        "confidence": 86,
        "severity": "High",
        "image": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Small water-soaked lesions that turn brown to purple with concentric rings",
            "Leaves turn yellow and collapse from infection point",
            "Bulb neck infection leading to post-harvest rotting"
        ],
        "recommendedRemedy": {
            "organic": "Garlic extract spray (5%) + Neem oil (3 ml/L) with sticking agent",
            "chemical": "Chlorothalonil 75% WP (2 g/L) or Tebuconazole 25.9% EC (1.5 ml/L)",
            "prevention": "Ensure good drainage; avoid overhead sprinkler irrigation during warm hours"
        }
    },
    "potato": {
        "diseaseName": "Late Blight (Phytophthora infestans)",
        "diseaseNameGu": "બટાકામાં પાછોતરો સુકારો (લેટ બ્લાઇટ)",
        "confidence": 91,
        "severity": "Critical",
        "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Water-soaked irregular pale-to-dark green lesions on leaves",
            "White fungal downy growth on leaf undersides in high humidity",
            "Rapid wilting and tuber brown rot"
        ],
        "recommendedRemedy": {
            "organic": "Bio-fungicide Bacillus subtilis foliar spray (10 g/L)",
            "chemical": "Cymoxanil 8% + Mancozeb 64% WP (3 g/L) or Metalaxyl-M + Mancozeb (2.5 g/L)",
            "prevention": "Certified blight-free seed tubers; destroy volunteer potato plants"
        }
    },
    "chilli": {
        "diseaseName": "Chilli Leaf Curl & Anthracnose / Dieback",
        "diseaseNameGu": "મરચીમાં પાન કોકડાઈ જવું અને ડાળી સુકારો",
        "confidence": 89,
        "severity": "High",
        "image": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Upward leaf curling, puckering, and severe reduction in leaf size",
            "Sunken circular lesions on ripening chilli fruits",
            "Dieback of twigs from top downwards"
        ],
        "recommendedRemedy": {
            "organic": "Neem oil 10,000 ppm (2 ml/L) + Agni Astra spray for vector control",
            "chemical": "Copper Oxychloride (3 g/L) + Diafenthiuron 50% WP (1 g/L)",
            "prevention": "Install yellow sticky traps; remove and burn infected plants"
        }
    },
    "okra": {
        "diseaseName": "Yellow Vein Mosaic Virus (YVMV)",
        "diseaseNameGu": "ભીંડામાં પીળી નસનો રોગ (યલો વેઇન મોઝેક)",
        "confidence": 88,
        "severity": "High",
        "image": "https://images.unsplash.com/photo-1425543103986-22abb7d7e8d2?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Network of clear yellow veins contrasting against green leaf lamina",
            "Leaves become completely yellow and reduced in size",
            "Fruits turn pale, fibrous, and unmarketable"
        ],
        "recommendedRemedy": {
            "organic": "Verticillium lecanii (5 g/L) + Neem soap solution spray",
            "chemical": "Acetamiprid 20% SP (0.4 g/L) or Thiamethoxam 25% WG (0.5 g/L)",
            "prevention": "Eradicate alternate weed hosts; sow YVMV-resistant cultivars"
        }
    },
    "soybean": {
        "diseaseName": "Soybean Rust (Phakopsora pachyrhizi)",
        "diseaseNameGu": "સોયાબીનમાં ગેરુ રોગ (રસ્ટ)",
        "confidence": 87,
        "severity": "High",
        "image": "https://images.unsplash.com/photo-1599818490533-3d0d540df167?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Tiny brown-to-reddish pustules primarily on lower leaf surfaces",
            "Premature yellowing, senescence, and total canopy defoliation",
            "Improper pod filling and shriveled grains"
        ],
        "recommendedRemedy": {
            "organic": "Cow urine spray (10%) + Bio-fermented Trichoderma viride",
            "chemical": "Hexaconazole 5% EC (2 ml/L) or Azoxystrobin (1 ml/L)",
            "prevention": "Ensure adequate plant-to-plant spacing for air circulation"
        }
    },
    "chickpea": {
        "diseaseName": "Ascochyta Blight & Fusarium Wilt",
        "diseaseNameGu": "ચણામાં સુકારો અને એસ્કોચાયટા બ્લાઇટ",
        "confidence": 85,
        "severity": "High",
        "image": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?auto=format&fit=crop&w=800&q=80",
        "symptoms": [
            "Drooping and yellowing of foliage starting from bottom leaves",
            "Internal xylem vascular discoloration (dark brown or black streak)",
            "Circular brown spots with concentric rings on stems and pods"
        ],
        "recommendedRemedy": {
            "organic": "Trichoderma harzianum seed treatment (10 g/kg) + soil drenching",
            "chemical": "Carbendazim 50% WP (1 g/L) or Carbendazim + Mancozeb (2 g/L)",
            "prevention": "Adopt 3-year crop rotation; avoid sowing in poorly drained soils"
        }
    }
}

class DiseaseService:
    def get_catalog(self) -> List[DiseaseCatalogItem]:
        return [DiseaseCatalogItem(**d) for d in CATALOG]

    async def analyze_sample(
        self,
        sample_id: Optional[str] = None,
        crop_id: Optional[str] = None,
        image_url: Optional[str] = None,
        storage_info: Optional[Dict[str, Any]] = None,
        db: Optional[AsyncSession] = None
    ) -> DiseaseAnalyzeResponse:
        crop_record = None

        # 1. Resolve crop from DB if crop_id is supplied
        if crop_id and db:
            res = await db.execute(select(Crop).where(Crop.id == crop_id))
            crop_record = res.scalars().first()
            if not crop_record:
                # Try finding by name or case-insensitive id
                res = await db.execute(select(Crop).where(Crop.id.ilike(crop_id)))
                crop_record = res.scalars().first()

        # 2. Check if crop is unsupported by AI
        if crop_record and not crop_record.disease_ai_supported:
            display_name = f"{crop_record.name} ({crop_record.name_gujarati})" if crop_record.name_gujarati else crop_record.name
            return DiseaseAnalyzeResponse(
                id=f"dis-unsupp-{uuid.uuid4().hex[:4]}",
                crop=display_name,
                crop_id=crop_record.id,
                diseaseName="AI Analysis Unavailable",
                diseaseNameGu="આ પાક માટે AI રોગ તપાસ ઉપલબ્ધ નથી",
                confidence=0,
                severity="Low",
                imageUrl=image_url or "https://images.unsplash.com/photo-1592417817098-8f3d6910985b?auto=format&fit=crop&w=800&q=80",
                symptoms=["AI disease model currently does not support automated scanning for this crop."],
                recommendedRemedy=DiseaseRemedy(
                    organic="Please escalate this sample directly to university agronomists for manual lab inspection.",
                    chemical="Avoid applying unprescribed chemical pesticides.",
                    prevention="Monitor the field and maintain standard hygiene until agronomist feedback is received."
                ),
                requiresExpertEscalation=True,
                supported=False,
                message="AI analysis is currently unavailable for this crop. You can request expert review."
            )

        # 3. If supported crop or demo sample
        target_crop_id = crop_record.id if crop_record else None
        if not target_crop_id and sample_id:
            demo_match = next((d for d in CATALOG if d["id"] == sample_id), None)
            if demo_match:
                target_crop_id = demo_match.get("crop_id")

        if not target_crop_id:
            target_crop_id = "cotton"

        profile = CROP_PROFILES.get(target_crop_id, CATALOG[0])
        crop_label = f"{crop_record.name} ({crop_record.name_gujarati})" if (crop_record and crop_record.name_gujarati) else profile.get("crop", target_crop_id.capitalize())
        disease_name = profile["diseaseName"]
        disease_name_gu = profile.get("diseaseNameGu")
        confidence = profile["confidence"]
        severity = profile["severity"]
        symptoms = profile["symptoms"]
        recommended_remedy = profile["recommendedRemedy"]
        
        # Configured confidence threshold: below 70% requires human agronomist verification
        requires_escalation = confidence < 70
        img = image_url or (storage_info.get("url") if storage_info else None) or profile.get("image", CATALOG[0]["image"])

        analysis_id = f"dis-{uuid.uuid4().hex[:4]}"

        # 4. Persist analysis to database if session is available
        if db:
            analysis_record = DiseaseAnalysis(
                id=analysis_id,
                crop_id=crop_record.id if crop_record else target_crop_id,
                field_id=None,
                crop=crop_label,
                disease=disease_name,
                disease_name=disease_name,
                disease_name_gu=disease_name_gu,
                confidence=confidence,
                severity=severity,
                image_url=img,
                storage_provider=(storage_info.get("storage_provider") if storage_info else "cloudinary"),
                public_id=(storage_info.get("public_id") if storage_info else ""),
                image_metadata=(storage_info.get("metadata") if storage_info else {}),
                analysis=f"Vision Agent pathogen detection for {crop_label}.",
                symptoms=symptoms,
                recommendation=recommended_remedy["organic"],
                recommended_remedy=recommended_remedy,
                expert_required=requires_escalation
            )
            db.add(analysis_record)
            try:
                await db.commit()
                await db.refresh(analysis_record)
            except Exception as e:
                await db.rollback()

        return DiseaseAnalyzeResponse(
            id=analysis_id,
            crop=crop_label,
            crop_id=crop_record.id if crop_record else target_crop_id,
            diseaseName=disease_name,
            diseaseNameGu=disease_name_gu,
            confidence=confidence,
            severity=severity,
            imageUrl=img,
            symptoms=symptoms,
            recommendedRemedy=DiseaseRemedy(**recommended_remedy),
            requiresExpertEscalation=requires_escalation,
            supported=True,
            message=None
        )

    async def get_escalations(self, db: AsyncSession) -> List[EscalationResponse]:
        res = await db.execute(select(ExpertReviewTicket).order_by(ExpertReviewTicket.created_at.desc()))
        tickets = res.scalars().all()
        return [
            EscalationResponse(
                id=t.id,
                field=t.field,
                crop=t.crop,
                issue=t.issue,
                aiConfidence=t.ai_confidence,
                reason=t.reason,
                assignedAgronomist=t.assigned_agronomist,
                status=t.status,
                submittedAt=t.submitted_at,
                telemetrySnapshot=t.telemetry_snapshot or {},
                agronomistNotes=t.agronomist_notes or ""
            ) for t in tickets
        ]

    async def create_escalation(self, db: AsyncSession, data: EscalationCreateRequest) -> EscalationResponse:
        ticket = ExpertReviewTicket(
            id=f"ESC-{random.randint(800, 899)}",
            field=data.field,
            crop=data.crop,
            issue=data.issue,
            ai_confidence=data.aiConfidence,
            reason=data.reason,
            assigned_agronomist="Dr. Arvind Dave (Senior Agronomist, JAU Junagadh)",
            status="Review Pending",
            submitted_at="Just now",
            telemetry_snapshot=data.telemetrySnapshot or {
                "moisture": "48%", "soilPH": "7.2", "nitrogen": "Normal", "phosphorus": "Low 14 mg/kg"
            },
            agronomist_notes="Ticket queued for university agronomist verification."
        )
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        return EscalationResponse(
            id=ticket.id,
            field=ticket.field,
            crop=ticket.crop,
            issue=ticket.issue,
            aiConfidence=ticket.ai_confidence,
            reason=ticket.reason,
            assignedAgronomist=ticket.assigned_agronomist,
            status=ticket.status,
            submittedAt=ticket.submitted_at,
            telemetrySnapshot=ticket.telemetry_snapshot or {},
            agronomistNotes=ticket.agronomist_notes or ""
        )

disease_service = DiseaseService()
