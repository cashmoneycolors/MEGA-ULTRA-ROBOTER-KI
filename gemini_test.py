
import requests
import json

GEMINI_API_KEY = "DEIN_API_KEY_HIER"
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

headers = {
    "x-goog-api-key": GEMINI_API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Erkläre, wie KI funktioniert, in wenigen Sätzen."}
            ]
        }
    ]
}

response = requests.post(ENDPOINT, headers=headers, json=payload)
if response.ok:
    data = response.json()
    print("Antwort:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("\nNur Text:")
    print(data["candidates"][0]["content"]["parts"][0]["text"])
else:
    print("Fehler:", response.text)
