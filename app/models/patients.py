from sqlalchemy.orm import Base
from sqlalchemy import Column, Integer


class Patient(Base):
    __tablename__ = "Patients"
    id = Column(Integer, primary_key = True)