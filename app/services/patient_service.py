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
