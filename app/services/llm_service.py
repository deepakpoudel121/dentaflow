from app.llm import get_structured_chain, reply_chain

from app.schemas import ReplyInput, ReplyOutput


async def llm_service(body, clinic) -> str:
    chain = get_structured_chain()
    response = await chain.ainvoke({
            "clinic_name": clinic,
            "message": body
        })
    return response

async def generate_reply(reply: ReplyInput) -> ReplyOutput:
    chain = reply_chain()
    response = await chain.ainvoke({
        'clinic_name': reply.clinic_name,
        'intent': reply.intent,
        'extracted_datetime': reply.extracted_datetime,
        'patient_name': reply.extracted_name,
        'patient_phone': reply.patient_phone,
        'patient_msg': reply.patient_msg
    })
    return response