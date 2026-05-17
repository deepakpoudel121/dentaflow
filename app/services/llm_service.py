from app.llm import get_structured_chain, reply_chain

from app.schemas import ReplyInput, ReplyOutput


async def llm_service(body, clinic) -> str:
    chain = get_structured_chain()
    response = await chain.ainvoke({
            "clinic_name": clinic,
            "message": body
        })
    return response
# class ReplyInput(BaseModel):
#     intent: str
#     patient_msg: str
#     extracted_datetime: str | None
#     patient_name: str | None
#     patient_phone: str
#     clinic_name: str
async def generate_reply(reply: ReplyInput) -> ReplyOutput:
    chain = reply_chain()
    response = await chain.ainvoke({
        'clinic_name': reply.clinic_name,
        'intent': reply.intent,
        'extracted_datetime': reply.extracted_datetime,
        'patient_name': reply.patient_name,
        'patient_phone': reply.patient_phone,
        'patient_msg': reply.patient_msg
    })
    return response