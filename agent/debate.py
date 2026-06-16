from agent.providers.gemini import ask_gemini


def run_debate(
    question: str,
    gemini_response: str,
    deepseek_response: str,
) -> dict:

    prompt = f"""
Question:
{question}

Gemini said:
{gemini_response}

DeepSeek said:
{deepseek_response}

Explain:

1. Where Gemini is stronger.
2. Where DeepSeek is stronger.
3. What each model would criticize about the other answer.
4. Produce a final consensus answer.
"""

    result = ask_gemini(prompt)

    return {
        "debate": result
    }