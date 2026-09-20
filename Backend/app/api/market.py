from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.market_service import market_service
from app.schemas.market import (
    CommodityResponse,
    PriceHistoryItem,
    NearbyMarketItem,
    PriceTrendResponse,
    MandiPricesResponse
)

router = APIRouter(prefix="/market", tags=["Mandi Market Prices"])

@router.get("", response_model=List[CommodityResponse])
@router.get("/prices", response_model=List[CommodityResponse])
async def get_market_prices(
    crop: Optional[str] = Query(None, description="Optional commodity filter (e.g. Cotton, Wheat)"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve live / cached mandi prices across monitored commodities."""
    return await market_service.get_market_commodities(crop=crop, db=db)

@router.get("/history", response_model=List[PriceHistoryItem])
async def get_price_history(
    crop: str = Query("Cotton", description="Commodity name"),
    days: int = Query(7, ge=1, le=30, description="Number of days"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve historical daily price data for a crop."""
    return await market_service.get_price_history(crop=crop, days=days, db=db)

@router.get("/nearby", response_model=List[NearbyMarketItem])
async def get_nearby_mandis(
    crop: str = Query("Cotton", description="Commodity name"),
    ref_mandi: str = Query("Rajkot APMC", description="Reference local mandi"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve nearby mandi prices for price arbitrage comparison."""
    return await market_service.get_nearby_mandis(crop=crop, ref_mandi=ref_mandi, db=db)

@router.get("/trends", response_model=PriceTrendResponse)
async def get_price_trend(
    crop: str = Query("Cotton", description="Commodity name")
):
    """Compute price trend (UP/DOWN/STABLE) and percentage change."""
    return await market_service.get_price_trend(crop=crop)

@router.get("/mandi/{mandi}", response_model=MandiPricesResponse)
async def get_mandi_prices(mandi: str):
    """Retrieve all commodity prices for a specific APMC mandi."""
    return await market_service.get_mandi_prices(mandi=mandi)
