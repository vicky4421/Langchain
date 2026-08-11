from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal

load_dotenv()

model = init_chat_model(
    model="gemini-3.6-flash",
    model_provider="google_genai",
)

# result = model.invoke(
#     '''
#         The hardware is great, but the software feels bloated. There're too many preinstalled apps that i can't remove. Also the UI looks outdated compared to other brands. Hoping for software update to fix this.
#     '''
# )

# print(result.content)

'''
    Output:
    {'type': 'text', 'text': 'It sounds like you\'re describing a common frustration with many tech devices today—having excellent physical build quality ruined by a cluttered software experience. \n\nIf you are looking for a official-sounding **customer support response** to send to a user who wrote this, or if you are looking for **practical steps/workarounds** to fix these issues on your own device, here are both options:\n\n---\n\n### Option 1: Official Support / Community Response (If you are responding to a customer)\n\n> "Thank you for sharing your feedback with us! We\'re thrilled to hear that you love the hardware quality, but we completely understand your frustration regarding the software experience. \n>\n> We take feedback about preinstalled apps and UI design very seriously. While certain system apps currently cannot be fully uninstalled, you can **disable** many of them via *Settings > Apps* to prevent them from running in the background or taking up space in your app drawer. \n>\n> Our software and UX design teams are actively working on future updates to streamline the interface and improve customization. Feedback like yours directly influences our software roadmap, so we really appreciate you taking the time to voice this. Stay tuned for upcoming updates!"\n\n---\n\n### Option 2: How to fix/mitigate this on your device right now\n\nIf this is your personal device, here are a few things you can do to clean up the software without waiting for an official up
    ...
'''

# Structured output in dictionary format

# Structure / Schema
# class Review(TypedDict):
#     summary: str
#     sentiment: str

# structured_model = model.with_structured_output(Review)

# result = structured_model.invoke(
#     '''
#         The hardware is great, but the software feels bloated. There're too many preinstalled apps that i can't       remove. Al
#     '''
# )

# print(result)
# print(f'summary: {result['summary']}')
# print(f'sentiment: {result['sentiment']}')

'''
    Output:
        {'summary': 'The user praises the hardware but complains about bloated software and unremovable preinstalled apps.', 'sentiment': 'mixed'}

    type of 'result' is dict, so we can extract values using keys.

    Output:
        {'summary': 'The user praises the hardware quality but complains about bloated software and unremovable preinstalled apps.', 'sentiment': 'mixed'}
        summary: The user praises the hardware quality but complains about bloated software and unremovable preinstalled apps.
        sentiment: mixed
'''

# Annotated and Optional and Literal
'''
    In Python, the term "annotated" typically refers to Type Annotations (or Type Hints), which allow you to explicitly declare the data types of variables, function arguments, and return values
    i.e. typing.Annotated lets you add arbitrary metadata to a type hint. The first argument is the actual data type, and everything after it is metadata
    with this we can put constraints to any variable or returns from function
    e.g.
    # The type checker sees an 'int', but libraries can read the validation string
    Age = Annotated[int, "Value must be between 0 and 120"]

    In our case we can guide llm for the desired output OR put constraints for output that we want to use in our program

    The output can be kept optional using Optional

    If we're expecting the output which is defined before we can use Literal
    e.g. in above response the sentiment is mixed if we want it neutral we can make it literal.
'''

class Review(TypedDict):
    key_themes: Annotated[list[str], 'Write down all key themes discussed in review in a list']
    summary: Annotated[str, 'A brief summary of review']
    sentiment: Annotated[Literal['neg', 'pos', 'neutral'], 'Return sentiment of review either negative, positive or neutral']
    pros: Annotated[Optional[list[str]], 'Write down all the pros inside a list']
    cons: Annotated[Optional[list[str]], 'Write down all the cons inside a list']
    name: Annotated[Optional[str], 'Write down name of the reviewer']

structured_model = model.with_structured_output(Review)

result = structured_model.invoke(
    '''
        I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it’s an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I’m gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

        The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it ofte       n. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

        However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung’s One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

        Pros:
        Insanely powerful processor (great for gaming and productivity)
        Stunning 200MP camera with incredible zoom capabilities
        Long battery life with fast charging
        S-Pen support is unique and useful

        Cons:
        Bulky and heavy: not great for one handed use
        Bloatware still exists in one UI
        Expensive compared to competitors
                                 
        Review by Vivek Sawant
    '''
)

print(f'key_themes: {result['key_themes']}')
print(f'summary: {result['summary']}')
print(f'sentiment: {result['sentiment']}')
print(f'pros: {result['pros']}')
print(f'cons: {result['cons']}')

'''
    Output:
        key_themes: ['Performance', 'Camera Quality', 'Battery & Charging', 'Design & Ergonomics', 'Software & Bloatware', 'Pricing']
        summary: The Samsung Galaxy S24 Ultra is an exceptionally powerful smartphone boasting top-tier performance, outstanding camera capabilities, excellent battery life, and S-Pen functionality, though its large size, heavy weight, software bloatware, and high price tag may deter some users.
        sentiment: pos
        pros: ['Insanely powerful processor (great for gaming and productivity)', 'Stunning 200MP camera with incredible zoom capabilities', 'Long battery life with fast charging', 'S-Pen support is unique and useful']
        cons: ['Bulky and heavy: not great for one handed use', 'Bloatware still exists in one UI', 'Expensive compared to competitors']

        Note: sentiment is literal
            : name is optional and didn't existed in review, so not returned
'''