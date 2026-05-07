from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path
from app.schemas import IntentClassification

load_dotenv()


def load_prompt(name: str) -> str:
    path = Path(__file__).parent /  f"{name}.txt"
    return path.read_text()


classify = load_prompt('prompts/classify_v1')



classifier= ChatPromptTemplate.from_template(classify)

llm = ChatMistralAI(model = 'mistral-small-latest')
classifier_llm = llm.with_structured_output(IntentClassification)


classify_chain = classifier | classifier_llm


