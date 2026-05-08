from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_
from app.db import AsyncSessionLocal
from app.models import Appointment, Patient
from app.core import logger, settings
from twilio.rest import Client
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

ACCOUNT_SID = settings.twilio_account_sid
AUTH_TOKEN = settings.twilio_auth_token
TWILIO_PHONE = settings.phone_number
async def send_remainders():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    async with AsyncSessionLocal() as db:
        try:
            now_time = datetime.now(timezone.utc)
            in_24hrs = now_time + timedelta(hours =24)
            query = select(Appointment).where(
                Appointment.status =='confirmed',
                Appointment.scheduled_at <= in_24hrs,
                Appointment.scheduled_at >= now_time,
                Appointment.reminder_sent == False
            )
            result = await db.execute(query)
            finalresult = result.scalars().all()
        
            logger.info("Appointments to be remainded today", extra={
                "numbers": len(finalresult),
                "Date": now_time

            })
            for res in finalresult:
                query = select(Patient).where(Patient.id == res.patient_id)
                patients = await db.execute(query)
                patient_one = patients.scalars().first()
                client.messages.create(
                    body="Please dont forget your today's appointment",
                    to=f"whatsapp:{patient_one.phone}",
                    from_=f"whatsapp:{TWILIO_PHONE}"
                )
                res.reminder_sent = True
            await db.commit()
        except Exception as e:
            logger.error("Remainder Job Failed", extra={
                "error": str(e)
            })
    
def start_scheduler():
    scheduler.add_job(send_remainders,"interval", hours=1)
    scheduler.start()
    logger.info("scheduler started")
    
def stop_scheduler():
    scheduler.shutdown()
    logger.info("scheduler stopped")