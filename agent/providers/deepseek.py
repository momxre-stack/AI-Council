import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def ask_deepseek(prompt: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content