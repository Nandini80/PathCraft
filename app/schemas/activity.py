from pydantic import BaseModel, Field
from typing import Optional
from datetime import time

class ActivityBase(BaseModel):
    activity_name: str
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    day_id: int
    
    class Config:
        from_attributes = True