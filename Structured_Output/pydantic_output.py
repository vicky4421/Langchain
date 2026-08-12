from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal,Optional

load_dotenv()

model = init_chat_model(
    model="gemini-3.6-flash",
    model_provider="google_genai",
)

class Review(BaseModel):
    key_themes: list[str] = Field(description='Write down all key themes discussed in review in a list')
    summary: str = Field(description='A brief summary of review')
    sentiment: Literal['+ve', '-ve'] = Field(description='Return sentiment of review either negative, positive')
    pros: Optional[list[str]] = Field(default= None, description='Write down all the pros inside a list')
    cons: Optional[list[str]] = Field(default= None, description='Write down all the cons inside a list')
    name: Optional[str] = Field(default= None, description='Write down name of the reviewer')

# NOTE: should provide default value for Optional fields

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

print(result)

print(f'key_themes: {result.key_themes}')
print(f'summary: {result.summary}')
print(f'sentiment: {result.sentiment}')
print(f'pros: {result.pros}')
print(f'cons: {result.cons}')

print(type(result))

'''
Output:
    key_themes=['Performance', 'Battery and Charging', 'Camera Capabilities', 'Design and Ergonomics', 'Software and Bloatware', 'Price'] summary='The Samsung Galaxy S24 Ultra is an immensely powerful flagship smartphone featuring top-tier performance, outstanding camera features, long battery life, and S-Pen support, though it is held back slightly by its large size, pre-installed bloatware, and high price tag.' sentiment='+ve' pros=['Insanely powerful processor (great for gaming and productivity)', 'Stunning 200MP camera with incredible zoom capabilities', 'Long battery life with fast charging', 'S-Pen support is unique and useful'] cons=['Bulky and heavy: not great for one handed use', 'Bloatware still exists in one UI', 'Expensive compared to competitors'] name='Vivek Sawant'

    key_themes: ['Performance', 'Battery and Charging', 'Camera Capabilities', 'Design and Ergonomics', 'Software and Bloatware', 'Price']
    summary: The Samsung Galaxy S24 Ultra is an immensely powerful flagship smartphone featuring top-tier performance, outstanding camera features, long battery life, and S-Pen support, though it is held back slightly by its large size, pre-installed bloatware, and high price tag.
    sentiment: +ve
    pros: ['Insanely powerful processor (great for gaming and productivity)', 'Stunning 200MP camera with incredible zoom capabilities', 'Long battery life with fast charging', 'S-Pen support is unique and useful']
    cons: ['Bulky and heavy: not great for one handed use', 'Bloatware still exists in one UI', 'Expensive compared to competitors']

    <class '__main__.Review'>
'''