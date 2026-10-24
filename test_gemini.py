
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
else:
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents="Explain machine learning in two sentences."
        )
        print("SUCCESS!")
        print(response.text)
    except Exception as e:
        print("GEMINI ERROR:")
        print(type(e).__name__, str(e))
