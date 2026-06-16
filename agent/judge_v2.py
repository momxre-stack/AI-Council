import json

from agent.providers.gemini import ask_gemini


def judge_responses_v2(
    question: str,
    gemini_response: str,
    deepseek_response: str,
) -> dict:
    prompt = f"""
You are the judge in a multi-model AI council.

Question:
{question}

Gemini response:
{gemini_response}

DeepSeek response:
{deepseek_response}

Return ONLY valid JSON with this exact structure:
{{
  "agreement_score": 0,
  "needs_debate": true,
  "agreements": [],
  "differences": [],
  "more_complete_response": "",
  "final_answer": ""
}}

Rules:
- agreement_score must be an integer from 0 to 100.
- needs_debate must be true if agreement_score is below 70.
- agreements must be a list of short strings.
- differences must be a list of short strings.
- more_complete_response must be "gemini", "deepseek", or "tie".
- final_answer must combine the strongest parts of both responses.
- Do not include markdown.
- Do not include explanations outside JSON.
"""

    raw_response = ask_gemini(prompt).strip()

    start = raw_response.find("{")
    end = raw_response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            f"Judge did not return JSON: {raw_response}"
        )

    json_text = raw_response[start:end + 1]

    return json.loads(json_text)