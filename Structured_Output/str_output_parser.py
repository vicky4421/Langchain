'''
Agenda here is to see how string output parser helps to get result from llm in structured format.
It mainly used with the llm's that doesn't support structured output but only return the raw text but here we're using
gemini llm which supports structured output but also one goal we're achieving here how str output parser helps in
formatting output from first response to input for second response.
Output parsers works with chains.
'''

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = init_chat_model(
    model="gemini-3.6-flash",
    model_provider="google_genai",
)

# 1st prompt
template1 = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)

# 2nd prompt
template2 = PromptTemplate(
    template='Write a 5 line summary on the following text \n {text}',
    input_variables=['text']
)

'''
WITHOUT STRING OUTPUT PARSER AND CHAINS

    prompt1 = template1.invoke({'topic': 'Black Hole'})

    result1 = model.invoke(prompt1)

    print(f'Result 1: {result1.content}')

    prompt2 = template2.invoke({'text': result1.content})

    result2 = model.invoke(prompt2)

    print(f'Result 2: {result2.content}')


    Output:
        Result 1: [{'type': 'text', 'text': '# Scientific Report: The Physics, Structure, and Astrophysical Significance of Black Holes\n\n---\n\n## Executive Summary\nA **black hole** is an astrophysical object with a gravitational field so intense that no matter or electromagnetic radiation (including light) can escape from within its boundary. First conceptualized as theoretical anomalies in Albert Einstein’s General Theory of Relativity, black holes are now empirically confirmed to exist throughout the universe. They range from stellar-mass bodies to supermassive entities containing billions of solar masses. This report provides a detailed examination of black holes, detailing their theoretical foundations, mechanics, classification, physical structures, observational evidence, and central role in modern physics.\n\n---\n\n## 1. Historical and Theoretical Background\n\n### 1.1 Newtonian Concepts ("Dark Stars")\nThe concept of an object with gravity so strong that light could not escape was independently proposed in the late 18th century by English natural philosopher **John Michell** (1783) and French mathematician **Pierre-Simon Laplace** (1796). Using Newtonian gravity, they calculated that if an object were dense enough, its escape velocity would exceed the speed of light ($c$).\n\n### 1.2 General Relativity and the Schwarzschild Solution\nIn 1915, Albert Einstein published his **General Theory of Relativity**, describing gravity not as a Newtonian force, but as the curvature of spacetime caused by mass and energy. \n\nIn 1916, while serving on the German front in World War I, physicist **Karl Schwarzschild** derived the first exact solution to Einstein’s field e
        ...
        Result 2: [{'type': 'text', 'text': "Here is a 5-line summary of the text:\n\n1. Black holes are dense astrophysical objects with gravitational fields so intense that nothing, including light, can escape from within their event horizon.\n2. Rooted in Einstein's General Relativity and Schwarzschild's equations, they consist of a central singularity, an event horizon, and often feature surrounding accretion disks and jets.\n3. Categorized primarily by mass—ranging from stellar-mass to supermassive entities—black holes are fully defined by only three classical parameters: mass, charge, and spin.\n4. Though directly invisible, their existence is proven through X-ray binary emissions, star orbits, gravitational wave detections, and direct shadow imaging by the Event Horizon Telescope.\n5. Phenomena like Hawking radiation, the information loss paradox, and central singularities position black holes at the crucial intersection between General Relativity and Quantum Mechanics.", 'extras': {'signature': 'EpoXCpcXARFNMg/imDXysOLbjnF6Y/5LlRBXB5IabfMWhTIAz1ZodTX+GiuIJks7wa8L0/ACopDJJRJEOIcewVRTH43/PhUcLRBpSqPvfR68G0wUKClRxfyO2EOfg37WW2dmI1TUpTlTHUhWfhH46pLmhuyQpEACQIuLVE3MqE2ELzL88S1SX0Imq7uA5wEf9Sr3uox6g50xhR/ExycON957McUK
        ...
'''

# WITH STRING OUTPUT PARSER AND CHAINS

parser = StrOutputParser()

# Chain (Pipeline)

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({'topic': 'Black Hole'})

print(result)

'''
    Output:
        A black hole is a region of spacetime with gravity so intense that nothing, including light, can escape beyond its event horizon.
        Ranging from stellar-mass to supermassive types, they form through collapsing massive stars, galactic mergers, or early cosmic events.
        Defined entirely by their mass, charge, and spin, black holes also exhibit Hawking radiation, which creates theoretical paradoxes between quantum mechanics and general relativity.
        Astronomers detect them indirectly by tracking stellar dynamics, high-energy X-ray emissions, gravitational waves, and direct shadow imaging via the Event Horizon Telescope.
        Anchoring the centers of most galaxies, black holes play a vital role in galactic evolution and serve as essential cosmic laboratories for theoretical physics.
'''