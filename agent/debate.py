import json

from agent.providers.gemini import ask_gemini


def _parse_debate_json(raw_response: str) -> dict:
    raw_response = raw_response.strip()

    start = raw_response.find("{")
    end = raw_response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"Debate did not return JSON: {raw_response}")

    json_text = raw_response[start:end + 1]
    return json.loads(json_text)


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