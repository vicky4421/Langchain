'''
Product feedback sentiment analysis

                                   (-ve)
user feedback - model - analyze(+ve/-ve) --- model ---- negative response
                             |
                           model
                             |(+ve)
                          positive response
'''

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.runnables import RunnableBranch, RunnableLambda

load_dotenv()

model = init_chat_model('google_genai:gemini-3.5-flash')

parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Give the sentiment of feedback')

py_parser = PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
    template='Classify the sentiment of the following feedback into positive or negative \n {feedback} \n {format_instruction}',
    input_variables=['feedback'],
    partial_variables={'format_instruction': py_parser.get_format_instructions()}
)

# classifier chain: chain in which classification of the feedback will done by the llm
classifier_chain = prompt1 | model | py_parser

# result = classifier_chain.invoke({'feedback': 'This is a wonderful phone'})
# print(result)
# print(result.sentiment)
# print(type(result))

'''
Output:
    sentiment='positive'
    positive
    <class '__main__.Feedback'>
'''
'''
branch_chain = RunnableBranch(
    (condition1, if true then which chain should execute),
    (condition2, if true then which chain should execute),
    default_chain
)
'''

# prompt for +ve response
prompt2 = PromptTemplate(
    template='Write an appropriate Professional & Classic: response to this positive feedback \n {feedback}',
    input_variables=['feedback']
)

# prompt for -ve response
prompt3 = PromptTemplate(
    template='Write an appropriate Professional & Classic: response to this negative feedback \n {feedback}',
    input_variables=['feedback']
)

branch_chain = RunnableBranch(
    (lambda x:x.sentiment == 'positive', prompt2 | model | parser),
    (lambda x:x.sentiment == 'negative', prompt3 | model | parser),
    RunnableLambda(lambda x: 'could not find sentiment')              # we don't have a default case
)

chain = classifier_chain | branch_chain

result = chain.invoke({'feedback': 'This is the feedback from customer who bought the phone from our store, it says this is very good phone'})

print(result)
print('\n')
chain.get_graph().print_ascii()

'''
Output:
Here is a professional and classic response template you can use:

***

**Subject:** Thank you for your kind feedback

Dear [Name],

Thank you very much for taking the time to share your positive feedback with us.

We are delighted to hear that you had such a wonderful experience. Our team strives to deliver the highest standard of service, and it is incredibly rewarding to know we have met your expectations.

Your support means a great deal to us, and we look forward to the opportunity of serving you again in the future.

Sincerely,

[Your Name/Your Company Name]
[Your Title]


      +-------------+
      | PromptInput |
      +-------------+
             *
             *
             *
    +----------------+
    | PromptTemplate |
    +----------------+
             *
             *
             *
+------------------------+
| ChatGoogleGenerativeAI |
+------------------------+
             *
             *
             *
 +----------------------+
 | PydanticOutputParser |
 +----------------------+
             *
             *
             *
        +--------+
        | Branch |
        +--------+
             *
             *
             *
     +--------------+
     | BranchOutput |
     +--------------+
'''