from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
from app.schemas import IntentClassification, ReplyOutput

load_dotenv()


def load_prompt(name: str) -> str:
    path = Path(__file__).parent /  f"{name}.txt"
    return path.read_text()


classify = load_prompt('prompts/classify_v1')



classifier= ChatPromptTemplate.from_template(classify)

llm = ChatMistralAI(model = 'mistral-small-latest')

def get_structured_chain():
    return classifier | llm.with_structured_output(IntentClassification)


responder_text = load_prompt('prompts/respond_v1')
responder = ChatPromptTemplate.from_template(responder_text)

def reply_chain():
    return responder | llm.with_structured_output(ReplyOutput)