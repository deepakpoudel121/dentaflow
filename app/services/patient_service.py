from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Patient, Message
from app.core import logger

async def get_or_create_patient(phone: str, db: AsyncSession) -> Patient:
    clean_phone = phone.replace("whatsapp:","")
    try:
        result = await db.execute(
            select(Patient).where(Patient.phone == clean_phone)
        )
        patient = result.scalars().first()

        if not patient:
            patient = Patient(phone=clean_phone)
            db.add(patient)
            await db.commit()
            await db.refresh(patient)
            logger.info("new patient created", extra={
                "phone": phone,
                "id": patient.id
            })

        return patient

    except Exception as e:
        logger.error("failed to get or create patient", extra={
            "phone": clean_phone,
            "error": str(e)
        })
        raise


# class Message(Base):
#     __tablename__ = "messages"
#     id         = Column(Integer, primary_key=True)
#     patient_id = Column(Integer, ForeignKey("patients.id"))
#     role       = Column(String(20))  # "patient" or "assistant"
#     content    = Column(Text, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
async def save_message(id:int, role:str, message:str, db):
    new_msg = Message(
            patient_id = id,
            role = role,
            content = message
    )
    db.add(new_msg)
    await db.commit()

async def get_conversation_history(patient_id:int, db:AsyncSession, limit:int = 10) -> str:
    messages = await db.execute(select(Message)
                                .where(Message.patient_id == patient_id)
                                .order_by(Message.created_at.asc())
                                .limit(limit) 
                                )
    
    final_text = messages.scalars().all()
    string_text = '\n'.join([
                            f"{msg.role.capitalize()}: {msg.content}" 
                            for msg in final_text
                        ])
    return string_text