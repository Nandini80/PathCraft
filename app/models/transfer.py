from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database import Base

class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    departure_time = Column(Time, nullable=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    
    # SQLite-compatible timestamp defaults
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relationships
    day = relationship("Day", back_populates="transfers")