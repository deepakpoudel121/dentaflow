from fastapi import APIRouter, Depends, Form
from fastapi.responses import Response
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.llm import classify_chain
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os

router = APIRouter(prefix='/appointment')

class MessageSchema(BaseModel):
    message_content: str




@router.post("/webhook")
async def get_appointments(Body: str = Form(...)):
    incoming_msg = Body.strip().lower()

    response_msg = await classify_chain.ainvoke({
        "clinic_name": "Deepak's Clinic",
        "message": incoming_msg
    })

    response = MessagingResponse()
    message = response.message()

    if response_msg.intent == "new_appointment":
        content = "Please call 9865505 to book your appointment."
    elif response_msg.intent == "other":
        content = "Please specify your reason for the message."
    else:
        content = "Sorry, I didn't understand your request."

    message.body(content)

    return Response(
        content=str(response),
        media_type="application/xml"
    )


# # from twilio.rest import Client

# account_sid = os.getenv("TWILIO_ACCOUNT_SID")
# auth_token = "TWILIO_ACCOUNT_TOKEN"
# client = Client(account_sid, auth_token)

# message = client.messages.create(
#   from_='whatsapp:+14155238886',
#   content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
#   content_variables='{"1":"12/1","2":"3pm"}',
#   to='whatsapp:+9779865505986'
# )

# print(message.sid)