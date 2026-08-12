# topic from user -> llm -> detailed report -> llm -> 5 interesting points

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = init_chat_model('google_genai:gemini-3.5-flash')

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate 5 interesting from \n {text}',
    input_variables=['text']
)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({'topic': 'Indian Cricket'})

print(result)
print('\n')
chain.get_graph().print_ascii()

'''
Output:
1. **Massive Financial Influence:** The Board of Control for Cricket in India (BCCI) is the wealthiest cricket board in the world, single-handedly contributing an estimated **70% to 80% of the International Cricket Council’s (ICC) global revenue**.
2. **The Multi-Billion Dollar IPL:** By 2023, the Indian Premier League's (IPL) brand valuation reached **$15.4 billion**. Its media rights for the 2023–2027 cycle were sold for **$6.2 billion**, making it one of the most expensive sports leagues in the world on a per-match basis, rivaling the NFL and the English Premier League.
3. **Pioneering Women's Sports:** Launched in 2023, the Women’s Premier League (WPL) has already established itself as the **most lucrative women’s sports league in the world outside of North America**.
4. **Historical Roots:** While India played its first official Test match in 1932, locals began adopting the sport much earlier. The Parsi community in Bombay was the first local community to take up cricket, founding the **Oriental Cricket Club in 1848**.
5. **The 11-Year Trophy Drought:** Despite its financial dominance and strong performance in bilateral series, the Indian men's national team went **11 years (from 2013 to 2024) without winning a single ICC trophy**, a streak that was finally broken with their T20 World Cup victory in 2024.


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
    +-----------------+
    | StrOutputParser |
    +-----------------+
             *
             *
             *
+-----------------------+
| StrOutputParserOutput |
+-----------------------+
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
    +-----------------+
    | StrOutputParser |
    +-----------------+
             *
             *
             *
+-----------------------+
| StrOutputParserOutput |
+-----------------------+
'''