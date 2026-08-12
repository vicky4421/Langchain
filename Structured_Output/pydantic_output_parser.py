'''
    Uses pydantic models to enforce schema validations.

    - Strict Scheme Enforcement
    - Type Safety: Automatically converts LLM outputs in python objects
    - Easy Validation
    - Seamless Integration
'''

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

model = init_chat_model(
    model="gemini-3.5-flash",
    model_provider="google_genai",
)

# Schema
class Person(BaseModel):
    name: str = Field(description='Name of the person')
    age: int = Field(gt=18, description='Age of the person')
    city: str = Field(description='Name of the city the person belongs to')

parser = PydanticOutputParser(pydantic_object= Person)

template = PromptTemplate(
    template='Generate the name, age and city of a fictional person from {place} \n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction': parser.get_config_jsonschema()}
)

chain = template | model | parser
result = chain.invoke({'place': 'UK'})

print(result)

'''
Output: name='Aniket Kulkarni' age=28 city='Pune'
'''