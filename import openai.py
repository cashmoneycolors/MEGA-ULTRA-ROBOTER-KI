import openai& "C:/Users/Laptop/Desktop/Projekte/MEGA ULTRA ROBOTER KI/ZENITH_FRONTEND/.venv/Scripts/python.exe" chat_test.py
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Sag Hallo!"}]
)
print(response.choices[0].message.content)