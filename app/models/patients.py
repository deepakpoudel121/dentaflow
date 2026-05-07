from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from app.db import Base


class Patient(Base):
    __tablename__ = "patients"
    
    id           = Column(Integer, primary_key=True)
    phone        = Column(String(20), unique=True, nullable=False)
    name         = Column(String(255), nullable=True)  # extracted by LLM later
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    appointments = relationship("Appointment", back_populates="patient")


