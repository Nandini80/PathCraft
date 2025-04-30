from pydantic import BaseModel
from typing import Optional
from datetime import time

class AccommodationBase(BaseModel):
    hotel_name: str
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None

class AccommodationCreate(AccommodationBase):
    pass

class Accommodation(AccommodationBase):
    id: int
    day_id: int
    
    class Config:
        from_attributes = True