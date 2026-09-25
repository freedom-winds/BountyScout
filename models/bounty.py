"""
BountyScout Database Models
Extended with bounty alert tracking.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Bounty(Base):
    __tablename__ = "bounties"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    repository = Column(String(255), nullable=False)
    url = Column(String(512), unique=True, nullable=False)
    status = Column(String(50), default="open")
    assigned_to = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    scanned_at = Column(DateTime)
    priority_score = Column(Integer, default=1)
    bounty_amount = Column(Float)
    source_metadata = Column(Text)


class BountyAlert(Base):
    __tablename__ = "bounty_alerts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    repository = Column(String(255), nullable=False)
    url = Column(String(512), unique=True, nullable=False)
    priority = Column(Integer, nullable=False)
    comments = Column(Integer, default=0)
    updated_at = Column(DateTime, nullable=False)
    bounty_amount = Column(Float)
    assigned_at = Column(DateTime)
    
    bounty = relationship("Bounty", uselist=False, backref="alert")