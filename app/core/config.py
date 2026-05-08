from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    mistral_api_key: str = ""
    groq_api_key: str = ""
    debug: bool = False
    clinic_name: str = "Deepak's Clinic"
    twilio_auth_token: str
    twilio_account_sid: str
    phone_number: str
    class Config:
        env_file = ".env"

settings = Settings()