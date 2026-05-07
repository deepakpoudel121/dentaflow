
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