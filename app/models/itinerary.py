from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import json

from app.database import Base

class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    nights = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    _highlights = Column("highlights", Text, nullable=True)
    price_estimate = Column(DECIMAL(10, 2), nullable=True)
    _tags = Column("tags", Text, nullable=True)
    is_recommended = Column(Boolean, default=False)
    
    # SQLite-compatible timestamp defaults
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relationships
    days = relationship("Day", back_populates="itinerary", cascade="all, delete-orphan")
    
    # Property methods for JSON serialization
    @property
    def highlights(self):
        if not self._highlights:
            return []
        try:
            return json.loads(self._highlights)
        except:
            return []
        
    @highlights.setter
    def highlights(self, value):
        if value is None:
            self._highlights = None
        else:
            self._highlights = json.dumps(value)
        
    @property
    def tags(self):
        if not self._tags:
            return []
        try:
            return json.loads(self._tags)
        except:
            return []
        
    @tags.setter
    def tags(self, value):
        if value is None:
            self._tags = None
        else:
            self._tags = json.dumps(value)