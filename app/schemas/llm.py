
from pydantic import BaseModel
from typing import Literal

class IntentClassification(BaseModel):
    intent: Literal[
        "new_appointment",
        "reschedule", 
        "cancel",
        "question",
        "other"
    ]
    extracted_datetime: str | None  
    extracted_name: str | None      
    confidence: Literal["high", "medium", "low"]

class ReplyOutput(BaseModel):
    message: str
    requires_human: Literal[True, False]
    action: Literal['none', 'create_appointment', 'notify_staff', 'collect_more_information']


class ReplyInput(BaseModel):
    intent: str
    patient_msg: str
    extracted_datetime: str | None
    patient_name: str | None
    patient_phone: str
    clinic_name: str