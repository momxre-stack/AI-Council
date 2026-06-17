import os
import time

from dotenv import load_dotenv
from openai import APIError, APITimeoutError, RateLimitError
from openai import OpenAI

load_dotenv()


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def ask_deepseek(prompt: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )

            return response.choices[0].message.content

        except (APIError, APITimeoutError, RateLimitError) as error:
            last_error = error

            if attempt == MAX_RETRIES - 1:
                break

            time.sleep(RETRY_DELAY_SECONDS)

    raise last_error