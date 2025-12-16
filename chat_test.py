import os
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY fehlt in .env/Umgebung")

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
    except Exception:
        import openai

        client = openai.OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "user", "content": "Sag Hallo!"}],
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
