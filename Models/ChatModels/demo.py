from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="gemini-3.6-flash",
    model_provider="google_genai",
)

print(model.invoke("What is the capital of India?").content)