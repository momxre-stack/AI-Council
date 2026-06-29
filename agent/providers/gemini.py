import os
import time

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError, UnknownApiResponseError

load_dotenv()


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
REQUEST_TIMEOUT_SECONDS = 30


def _parse_generate_content_response(response_data: dict) -> str:
    return response_data["candidates"][0]["content"]["parts"][0]["text"]


def _post_generate_content(api_key: str, prompt: str) -> dict:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-2.5-flash:generateContent?key={api_key}"
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = httpx.post(
        url,
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    return response.json()


def ask_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=REQUEST_TIMEOUT_SECONDS),
    )

    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            return response.text

        except (APIError, UnknownApiResponseError, TimeoutError, httpx.TimeoutException) as error:
            last_error = error

            if attempt == MAX_RETRIES - 1:
                break

            time.sleep(RETRY_DELAY_SECONDS)

    raise last_error