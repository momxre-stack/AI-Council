import json


def parse_json_object(raw_response: str, error_prefix: str) -> dict:
    cleaned_response = _strip_markdown_fence(raw_response.strip())

    start = cleaned_response.find("{")
    end = cleaned_response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"{error_prefix}: {raw_response}")

    json_text = cleaned_response[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as error:
        raise ValueError(f"{error_prefix}: {raw_response}") from error


def _strip_markdown_fence(raw_response: str) -> str:
    if not raw_response.startswith("```"):
        return raw_response

    lines = raw_response.splitlines()

    if len(lines) < 2 or not lines[-1].strip().startswith("```"):
        return raw_response

    return "\n".join(lines[1:-1]).strip()
