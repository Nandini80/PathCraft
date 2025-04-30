from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database import Base

class Day(Base):
    __tablename__ = "days"
    
    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    
    # SQLite-compatible timestamp defaults
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relationships
    itinerary = relationship("Itinerary", back_populates="days")
    accommodations = relationship("Accommodation", back_populates="day", cascade="all, delete-orphan")
    transfers = relationship("Transfer", back_populates="day", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="day", cascade="all, delete-orphan")