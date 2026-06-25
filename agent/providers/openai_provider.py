import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


REQUEST_TIMEOUT_SECONDS = 30


def ask_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    client = OpenAI(
        api_key=api_key,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content