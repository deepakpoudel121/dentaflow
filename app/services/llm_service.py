from app.llm import get_structured_chain, reply_chain

from app.schemas import  ReplyOutput


async def llm_service(body, clinic) -> dict:
    chain = get_structured_chain()
    response = await chain.ainvoke({
            "clinic_name": clinic,
            "message": body
        })
    return response

async def generate_reply(
    patient_message: str,
    intent: str,
    extracted_datetime: str | None,
    extracted_name: str | None,
    patient_phone: str,
    clinic_name: str,
    confidence:str,
    history_convo:str
) -> ReplyOutput:
    chain = reply_chain()
    response = await chain.ainvoke({
        'clinic_name': clinic_name,
        'intent': intent,
        'extracted_datetime': extracted_datetime,
        'patient_name': extracted_name,
        'patient_phone': patient_phone,
        'patient_msg': patient_message,
        'confidence': confidence,
        'history': history_convo
    })
    return response