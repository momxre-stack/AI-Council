from agent.json_utils import parse_json_object
from agent.providers.gemini import ask_gemini


def _parse_debate_json(raw_response: str) -> dict:
    return parse_json_object(raw_response, "Debate did not return JSON")


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

Return ONLY valid JSON with this exact structure:
{{
  "gemini_strengths": "",
  "deepseek_strengths": "",
  "criticisms": "",
  "consensus_answer": ""
}}

Rules:
- Return a single JSON object only.
- All values must be strings.
- Escape all quotation marks inside string values.
- Do not use unescaped newlines inside string values.
- Do not include markdown.
- Do not include code fences.
- Do not include explanations outside JSON.
- gemini_strengths must explain where Gemini's answer is stronger.
- deepseek_strengths must explain where DeepSeek's answer is stronger.
- criticisms must explain what each answer misses or gets wrong.
- consensus_answer must combine the strongest parts into one final answer.
"""

    result = ask_gemini(prompt)

    return _parse_debate_json(result)