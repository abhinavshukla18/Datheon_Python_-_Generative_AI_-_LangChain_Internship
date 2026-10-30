import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000),
)

response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents="Say hello in one short sentence.",
)
print(response.text)