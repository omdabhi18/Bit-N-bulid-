from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class NearbyMarketItem(BaseModel):
    name: str
    price: float
    distance: str
    arrivals: str

class PriceHistoryItem(BaseModel):
    day: str
    price: float

class CommodityResponse(BaseModel):
    id: str
    crop: str
    unit: str
    currentPrice: float
    change7d: float
    trend: str
    mspPrice: float
    aiRecommendation: str
    nearbyMarkets: List[NearbyMarketItem] = []
    priceHistory: List[PriceHistoryItem] = []
    
    # Extended fields
    mandi: Optional[str] = "Rajkot APMC"
    state: Optional[str] = "Gujarat"
    district: Optional[str] = "Rajkot"
    commodity: Optional[str] = None
    variety: Optional[str] = None
    minPrice: Optional[float] = None
    maxPrice: Optional[float] = None
    modalPrice: Optional[float] = None
    arrivalQuantity: Optional[str] = None
    source: Optional[str] = "Agmarknet OGD"
    status: Optional[str] = "available"

class PriceTrendResponse(BaseModel):
    crop: str
    currentPrice: float
    trend: str
    change7d: float
    source: str
    status: str = "available"

class MandiPricesResponse(BaseModel):
    mandi: str
    prices: List[CommodityResponse]
    totalCommodities: int
    source: str
