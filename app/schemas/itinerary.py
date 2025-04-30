from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from app.schemas.day import Day, DayCreate

class ItineraryBase(BaseModel):
    name: str
    region: str
    nights: int
    description: Optional[str] = None
    highlights: Optional[List[str]] = []
    price_estimate: Optional[Decimal] = None
    tags: Optional[List[str]] = []
    is_recommended: Optional[bool] = False

class ItineraryCreate(ItineraryBase):
    days: List[DayCreate]

class Itinerary(ItineraryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    days: List[Day] = []
    
    class Config:
        from_attributes = True

class ItineraryResponse(BaseModel):
    success: bool = True
    data: Optional[Itinerary] = None
    message: Optional[str] = None

class ItinerariesResponse(BaseModel):
    success: bool = True
    count: int
    data: List[Itinerary]