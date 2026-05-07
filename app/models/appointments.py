from datetime import datetime
import enum

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base



class AppointmentStatus(str, enum.Enum):
    pending   = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"
    no_show   = "no_show"

class Appointment(Base):
    __tablename__ = "appointments"
    
    id              = Column(Integer, primary_key=True)
    patient_id      = Column(Integer, ForeignKey("patients.id"))
    scheduled_at    = Column(DateTime(timezone=True), nullable=True)
    status          = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending)
    notes           = Column(Text, nullable=True)
    reminder_sent   = Column(Boolean, default=False)
    review_sent     = Column(Boolean, default=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    patient         = relationship("Patient", back_populates="appointments")