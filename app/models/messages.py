from datetime import datetime
import enum

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    String,
    Text,

)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base


class Message(Base):
    __tablename__ = "messages"
    id         = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    role       = Column(String(20))  # "patient" or "assistant"
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())