from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model = "gemini-embedding-2-preview",
    dimensions = 32
)

# vector = embeddings.embed_query("What is the capital of India?")

docs = [
    "What is the capital of India?",
    "What is the largest mammal?"
]

vector = embeddings.embed_documents(docs)

print(str(vector))