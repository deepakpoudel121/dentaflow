from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.core import logger, settings
from app.services import get_or_create_patient, llm_service, generate_reply
from twilio.twiml.messaging_response import MessagingResponse
from app.schemas import ReplyInput

router = APIRouter(prefix='/appointment')

@router.post("/webhook")
async def receive_message(
    Body: str = Form(...),
    From: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    logger.info("whatsapp message received", extra={
        "from": From,
        "message_length": len(Body)
    })

    try:
        # Step 1 — get or create patient
        patient = await get_or_create_patient(From, db)

        # Step 2 — classify intent
        result = await llm_service(Body,settings.clinic_name)
        logger.info("intent classified", extra={
            "from": From,
            "intent": result.intent,
            "confidence": result.confidence
        })
        input_msg = ReplyInput(
            intent= result.intent,
            clinic_name = settings.clinic_name,
            patient_msg = Body,
            patient_phone = From,
            extracted_datetime = result.extracted_datetime,
            patient_name = result.patient_name | None

        )
        # Step 3 — generate reply
        response = await generate_reply(input_msg)
        
 
        if response.require_human:
            print("Escalated to human")
        if response.action.lower() == 'create_appointment':
            print("Create Appointment Function Runs")
        elif response.action.lower() == 'notify_staff':
            print("Notify Staff Func")
        content = response.message
       

    except Exception as e:
        logger.error("webhook processing failed", extra={
            "from": From,
            "error": str(e)
        })
        content = (
            "Sorry, we're experiencing technical difficulties. "
            "Please call us directly."
        )

    # Step 4 — send TwiML response
    twiml = MessagingResponse()
    twiml.message(content)
    return Response(content=str(twiml), media_type="application/xml")