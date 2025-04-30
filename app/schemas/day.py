from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.schemas.accommodation import Accommodation, AccommodationCreate
from app.schemas.transfer import Transfer, TransferCreate
from app.schemas.activity import Activity, ActivityCreate

class DayBase(BaseModel):
    day_number: int
    date: date

class DayCreate(DayBase):
    accommodations: Optional[List[AccommodationCreate]] = []
    transfers: Optional[List[TransferCreate]] = []
    activities: Optional[List[ActivityCreate]] = []

class Day(DayBase):
    id: int
    itinerary_id: int
    accommodations: List[Accommodation] = []
    transfers: List[Transfer] = []
    activities: List[Activity] = []
    
    class Config:
        from_attributes = True