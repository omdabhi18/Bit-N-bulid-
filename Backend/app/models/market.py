from sqlalchemy import Column, String, Float, Integer, JSON, DateTime
from datetime import datetime, timezone
from app.database import Base

class MarketCommodity(Base):
    __tablename__ = "market_commodities"

    id = Column(String, primary_key=True) # e.g. "comm-cotton"
    crop = Column(String, nullable=False)
    unit = Column(String, default="₹ / Quintal (100 kg)")
    current_price = Column(Float, default=7380.0)
    change_7d = Column(Float, default=4.2)
    trend = Column(String, default="up")
    msp_price = Column(Float, default=7122.0)
    ai_recommendation = Column(String, default="")
    nearby_markets = Column(JSON, default=list) # [{ name, price, distance, arrivals }]
    price_history = Column(JSON, default=list)  # [{ day, price }]
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(String(50), primary_key=True)
    crop = Column(String(100), nullable=False)
    commodity = Column(String(100), nullable=True)
    variety = Column(String(100), nullable=True)
    mandi = Column(String(100), default="Rajkot APMC")
    state = Column(String(100), default="Gujarat")
    district = Column(String(100), default="Rajkot")
    location = Column(String(100), default="Rajkot, Gujarat")
    
    price = Column(Float, default=7380.0)
    min_price = Column(Float, default=7000.0)
    max_price = Column(Float, default=7500.0)
    modal_price = Column(Float, default=7380.0)
    arrival_quantity = Column(String(100), default="3,200 Qtl")
    
    unit = Column(String(50), default="₹ / Quintal (100 kg)")
    change_7d = Column(Float, default=4.2)
    trend = Column(String(20), default="UP")
    msp_price = Column(Float, default=7122.0)
    ai_recommendation = Column(String(255), default="")
    nearby_markets = Column(JSON, default=list)
    price_history = Column(JSON, default=list)
    source = Column(String(100), default="Agmarknet OGD")
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
