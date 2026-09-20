import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.integrations.market_provider import get_market_provider, MarketPriceProvider
from app.integrations.redis_cache import cache_service
from app.models.market import MarketPrice, MarketCommodity
from app.schemas.market import (
    CommodityResponse,
    NearbyMarketItem,
    PriceHistoryItem,
    PriceTrendResponse,
    MandiPricesResponse
)
from app.utils.logger import logger

class MarketService:
    def __init__(self):
        self.provider: MarketPriceProvider = get_market_provider()

    async def get_market_commodities(
        self,
        crop: Optional[str] = None,
        db: Optional[AsyncSession] = None
    ) -> List[CommodityResponse]:
        cache_key = f"market:commodities:{crop or 'all'}"
        cached = await cache_service.get_json(cache_key)
        if cached:
            return [CommodityResponse(**item) for item in cached]

        try:
            raw_items = await self.provider.get_current_prices(crop=crop)
            if not raw_items:
                raise ValueError("No market data returned from provider")
        except Exception as e:
            logger.warning(f"Market provider failed: {e}. Attempting DB fallback.")
            if db:
                db_items = await self._get_prices_from_db(db, crop)
                if db_items:
                    return db_items
            return [
                CommodityResponse(
                    id="unavailable",
                    crop=crop or "Market",
                    unit="₹ / Quintal",
                    currentPrice=0.0,
                    change7d=0.0,
                    trend="stable",
                    mspPrice=0.0,
                    aiRecommendation="Market data temporarily unavailable. Retrying connection...",
                    nearbyMarkets=[],
                    priceHistory=[],
                    status="unavailable"
                )
            ]

        results = []
        for item in raw_items:
            comp_item = CommodityResponse(
                id=item.get("id") or f"comm-{uuid.uuid4().hex[:6]}",
                crop=item.get("crop", "Unknown"),
                unit=item.get("unit", "₹ / Quintal"),
                currentPrice=float(item.get("currentPrice", 0.0)),
                change7d=float(item.get("change7d", 0.0)),
                trend=item.get("trend", "stable"),
                mspPrice=float(item.get("mspPrice", 0.0)),
                aiRecommendation=item.get("aiRecommendation", "Favorable market conditions."),
                nearbyMarkets=[NearbyMarketItem(**m) for m in item.get("nearbyMarkets", [])],
                priceHistory=[PriceHistoryItem(**h) for h in item.get("priceHistory", [])],
                mandi=item.get("mandi", "Rajkot APMC"),
                state=item.get("state", "Gujarat"),
                district=item.get("district", "Rajkot"),
                commodity=item.get("commodity"),
                variety=item.get("variety"),
                minPrice=item.get("minPrice"),
                maxPrice=item.get("maxPrice"),
                modalPrice=item.get("modalPrice"),
                arrivalQuantity=item.get("arrivalQuantity"),
                source=item.get("source", "Agmarknet OGD"),
                status="available"
            )
            results.append(comp_item)

            if db:
                await self._persist_market_price(db, comp_item)

        await cache_service.set_json(cache_key, [r.model_dump() for r in results], expire_seconds=3600)
        return results

    async def get_price_history(
        self,
        crop: str,
        days: int = 7,
        db: Optional[AsyncSession] = None
    ) -> List[PriceHistoryItem]:
        cache_key = f"market:history:{crop}:{days}"
        cached = await cache_service.get_json(cache_key)
        if cached:
            return [PriceHistoryItem(**i) for i in cached]

        try:
            history = await self.provider.get_price_history(crop, days)
            res = [PriceHistoryItem(**h) for h in history]
            await cache_service.set_json(cache_key, [r.model_dump() for r in res], expire_seconds=3600)
            return res
        except Exception as e:
            logger.warning(f"Error fetching history for {crop}: {e}")
            commodities = await self.get_market_commodities(crop=crop, db=db)
            if commodities and commodities[0].priceHistory:
                return commodities[0].priceHistory[-days:]
            return []

    async def get_nearby_mandis(
        self,
        crop: str,
        ref_mandi: str = "Rajkot APMC",
        db: Optional[AsyncSession] = None
    ) -> List[NearbyMarketItem]:
        cache_key = f"market:nearby:{crop}:{ref_mandi}"
        cached = await cache_service.get_json(cache_key)
        if cached:
            return [NearbyMarketItem(**m) for m in cached]

        try:
            mandis = await self.provider.get_nearby_mandis(crop, ref_mandi)
            res = [NearbyMarketItem(**m) for m in mandis]
            await cache_service.set_json(cache_key, [r.model_dump() for r in res], expire_seconds=3600)
            return res
        except Exception as e:
            logger.warning(f"Error fetching nearby mandis for {crop}: {e}")
            commodities = await self.get_market_commodities(crop=crop, db=db)
            if commodities and commodities[0].nearbyMarkets:
                return commodities[0].nearbyMarkets
            return []

    async def get_price_trend(self, crop: str) -> PriceTrendResponse:
        try:
            trend_data = await self.provider.get_price_trend(crop)
            return PriceTrendResponse(
                crop=trend_data.get("crop", crop),
                currentPrice=float(trend_data.get("currentPrice", 0.0)),
                trend=trend_data.get("trend", "stable"),
                change7d=float(trend_data.get("change7d", 0.0)),
                source=trend_data.get("source", "Agmarknet"),
                status="available"
            )
        except Exception as e:
            logger.warning(f"Error calculating price trend for {crop}: {e}")
            return PriceTrendResponse(
                crop=crop,
                currentPrice=0.0,
                trend="stable",
                change7d=0.0,
                source="System Fallback",
                status="unavailable"
            )

    async def get_mandi_prices(self, mandi: str) -> MandiPricesResponse:
        commodities = await self.get_market_commodities()
        filtered = [c for c in commodities if mandi.lower() in (c.mandi or "").lower()]
        return MandiPricesResponse(
            mandi=mandi,
            prices=filtered or commodities,
            totalCommodities=len(filtered or commodities),
            source="Agmarknet APMC Feed"
        )

    async def _persist_market_price(self, db: AsyncSession, item: CommodityResponse):
        try:
            res = await db.execute(select(MarketPrice).where(MarketPrice.id == item.id))
            existing = res.scalars().first()
            if existing:
                existing.price = item.currentPrice
                existing.modal_price = item.modalPrice or item.currentPrice
                existing.min_price = item.minPrice or item.currentPrice * 0.95
                existing.max_price = item.maxPrice or item.currentPrice * 1.05
                existing.change_7d = item.change7d
                existing.trend = item.trend
                existing.ai_recommendation = item.aiRecommendation
                existing.nearby_markets = [m.model_dump() for m in item.nearbyMarkets]
                existing.price_history = [h.model_dump() for h in item.priceHistory]
                existing.source = item.source or "Agmarknet OGD"
                existing.date = datetime.now(timezone.utc)
            else:
                new_price = MarketPrice(
                    id=item.id,
                    crop=item.crop,
                    commodity=item.commodity,
                    variety=item.variety,
                    mandi=item.mandi or "Rajkot APMC",
                    state=item.state or "Gujarat",
                    district=item.district or "Rajkot",
                    location=f"{item.mandi or 'Rajkot'}, Gujarat",
                    price=item.currentPrice,
                    modal_price=item.modalPrice or item.currentPrice,
                    min_price=item.minPrice or item.currentPrice * 0.95,
                    max_price=item.maxPrice or item.currentPrice * 1.05,
                    arrival_quantity=item.arrivalQuantity or "150 Qtl",
                    unit=item.unit,
                    change_7d=item.change7d,
                    trend=item.trend,
                    msp_price=item.mspPrice,
                    ai_recommendation=item.aiRecommendation,
                    nearby_markets=[m.model_dump() for m in item.nearbyMarkets],
                    price_history=[h.model_dump() for h in item.priceHistory],
                    source=item.source or "Agmarknet OGD",
                    date=datetime.now(timezone.utc)
                )
                db.add(new_price)
            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to persist market price to DB: {e}")

    async def _get_prices_from_db(self, db: AsyncSession, crop: Optional[str] = None) -> List[CommodityResponse]:
        try:
            stmt = select(MarketPrice)
            if crop:
                stmt = stmt.where(MarketPrice.crop.ilike(f"%{crop}%"))
            res = await db.execute(stmt)
            rows = res.scalars().all()
            if not rows:
                return []
            return [
                CommodityResponse(
                    id=r.id,
                    crop=r.crop,
                    unit=r.unit,
                    currentPrice=r.price,
                    change7d=r.change_7d,
                    trend=r.trend.lower() if r.trend else "stable",
                    mspPrice=r.msp_price,
                    aiRecommendation=r.ai_recommendation,
                    nearbyMarkets=[NearbyMarketItem(**m) for m in (r.nearby_markets or [])],
                    priceHistory=[PriceHistoryItem(**h) for h in (r.price_history or [])],
                    mandi=r.mandi,
                    state=r.state,
                    district=r.district,
                    commodity=r.commodity,
                    variety=r.variety,
                    minPrice=r.min_price,
                    maxPrice=r.max_price,
                    modalPrice=r.modal_price,
                    arrivalQuantity=r.arrival_quantity,
                    source=f"{r.source} (Cached from DB)",
                    status="cached"
                )
                for r in rows
            ]
        except Exception as e:
            logger.error(f"Error reading market prices from DB: {e}")
            return []

market_service = MarketService()
