from agent.json_utils import parse_json_object
from agent.providers.gemini import ask_gemini


REQUIRED_DEBATE_FIELDS = {
    "gemini_strengths",
    "deepseek_strengths",
    "criticisms",
    "consensus_answer",
}


def _parse_debate_json(raw_response: str) -> dict:
    result = parse_json_object(raw_response, "Debate did not return JSON")

    missing_fields = REQUIRED_DEBATE_FIELDS - result.keys()

    if missing_fields:
        missing_list = ", ".join(sorted(missing_fields))
        raise ValueError(
            f"Debate response missing required fields: {missing_list}"
        )

    unexpected_fields = result.keys() - REQUIRED_DEBATE_FIELDS

    if unexpected_fields:
        unexpected_list = ", ".join(sorted(unexpected_fields))
        raise ValueError(
            f"Debate response contains unexpected fields: {unexpected_list}"
        )

    for field in REQUIRED_DEBATE_FIELDS:
        if not isinstance(result[field], str):
            raise ValueError(
                f"Debate response field '{field}' must be a string"
            )

        if not result[field].strip():
            raise ValueError(
                f"Debate response field '{field}' must not be empty"
            )

    return result


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
- Use exactly the four fields above.
- Do not add extra fields.
- All values must be strings.
- All values must be non-empty after trimming whitespace.
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