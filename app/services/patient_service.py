from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Patient
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

def generate_reply(intent: str, patient_name: str | None = None) -> str:
    greeting = f"Hi {patient_name}! " if patient_name else "Hi! "
    
    replies = {
        "new_appointment": f"{greeting}I'd love to help you book an appointment. What date and time works best for you?",
        "reschedule": f"{greeting}I can help you reschedule. What's your current appointment date and what new date would you prefer?",
        "cancel": f"{greeting}I can help cancel your appointment. Can you confirm your appointment date?",
        "question": f"{greeting}Thank you for your question. Our team will get back to you shortly, or you can call us directly.",
        "other": f"{greeting}Thank you for reaching out. How can we help you today?",
    }
    return replies.get(intent, "Thank you for your message. We'll be in touch shortly.")