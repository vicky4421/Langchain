from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

model = init_chat_model(
    model="gemini-3.6-flash",
    model_provider="google_genai",
)

parser = JsonOutputParser()

template = PromptTemplate(
    template='Give me name, age and city of a fictional person \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

'''
Above we're instructing the llm that what should be the output structure/format we're expecting by adding format_instruction variable in the prompt and passing it in partial variable
why partial variable?
coz it resolves before runtime unlike input variable at runtime
'''

prompt = template.format()

# print(prompt)

'''
    Give me name, age and city of a fictional person
    Return a JSON object.
'''
'''
chain = template | model | parser
result = chain.invoke({})
'''

chain = model | parser

result = chain.invoke(prompt)
print(result)

# Output: {'name': 'Elena Rostova', 'age': 29, 'city': 'Prague'}

'''
NOTE: You can't enforce an output schema like pydantic or json structured output.
'''