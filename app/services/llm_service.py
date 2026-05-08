from app.llm import get_chain

async def llm_service(body, clinic) -> str:
    chain = get_chain()
    response = await chain.ainvoke({
            "clinic_name": clinic,
            "message": body
        })
    return response