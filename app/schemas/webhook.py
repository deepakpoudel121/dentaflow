from pydantic import BaseModel

class MessageSchema(BaseModel):
    message_content: str