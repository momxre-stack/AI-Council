import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

load_dotenv()


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def ask_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    client = genai.Client(api_key=api_key)

    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            return response.text

        except ServerError as error:
            last_error = error

            if attempt == MAX_RETRIES - 1:
                break

            time.sleep(RETRY_DELAY_SECONDS)

    raise last_error