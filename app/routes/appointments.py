from fastapi import APIRouter, Depends
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.llm import classify_chain
from app.schemas import IntentClassification
router = APIRouter(prefix='/appointment')

class MessageSchema(BaseModel):
    message_content: str




@router.post('/', response_model=IntentClassification)
async def get_appointments(request: MessageSchema, db: AsyncSession = Depends(get_db)):
    response = await classify_chain.ainvoke({
        "clinic_name": "Deepak's Clinic",
        "message": request.message_content})

    return response