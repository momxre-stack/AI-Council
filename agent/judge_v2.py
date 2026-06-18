from agent.json_utils import parse_json_object
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

    raw_response = ask_gemini(prompt)

    return parse_json_object(raw_response, "Judge did not return JSON")