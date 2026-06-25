import os
import time

from dotenv import load_dotenv
from openai import APIError
from openai import OpenAI

load_dotenv()


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
REQUEST_TIMEOUT_SECONDS = 30


def ask_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    client = OpenAI(
        api_key=api_key,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )

            return response.choices[0].message.content

        except APIError as error:
            last_error = error

            if attempt == MAX_RETRIES - 1:
                break

            time.sleep(RETRY_DELAY_SECONDS)

    raise last_error