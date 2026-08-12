'''
    Structured Output Parser helps extract structered JSON data from llm responses based on predefined schema.
    It works by defining a list of fields (ResponseSchema) that the model should return, ensuring the output follows the structured format.

    NOTE: outputs provide by model..with_structured_output() is native api level supported by llms and highly reliable, requires low tokens while StructuredOutputParser relies on regex and string parsing on raw model output not reliable but no choice if llm doesn't provide reponse for structured output, requires more tokens as longer prompts.

    DEPRICATED IN MODERN VERSIONS
'''