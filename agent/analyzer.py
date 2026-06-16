from agent.providers.gemini import ask_gemini


def analyze_responses(
    question: str,
    gemini_response: str,
    deepseek_response: str,
) -> str:
    prompt = f"""
Question:
{question}

Gemini response:
{gemini_response}

DeepSeek response:
{deepseek_response}

Analyze these responses.

Provide:
1. Agreements
2. Differences
3. Which response is more complete
4. A final combined answer
"""

    return ask_gemini(prompt)