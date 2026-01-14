import os
from dotenv import load_dotenv
from google.genai import Client

# Load .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise SystemExit("❌ GOOGLE_API_KEY not found in .env")

# Create client
client = Client(api_key=API_KEY)

print("\n✅ Available Gemini Models:\n")

for model in client.models.list():
    print(model.name)
