from pydantic import BaseModel
from typing import Optional
from datetime import time

class TransferBase(BaseModel):
    from_location: str
    to_location: str
    departure_time: Optional[time] = None

class TransferCreate(TransferBase):
    pass

class Transfer(TransferBase):
    id: int
    day_id: int
    
    class Config:
        from_attributes = True