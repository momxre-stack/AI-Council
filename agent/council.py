from agent.providers.registry import PROVIDERS
from agent.dual_judge import run_dual_judgment
from agent.debate import run_debate
from agent.quota_utils import is_quota_error



def ask_gemini(prompt: str) -> str:
    return PROVIDERS["gemini"](prompt)


def ask_deepseek(prompt: str) -> str:
    return PROVIDERS["deepseek"](prompt)


def _ask_provider(provider_name: str, provider, question: str) -> dict:
    try:
        response = provider(question)

        if not isinstance(response, str):
            return {
                "provider": provider_name,
                "response": None,
                "error": "Provider returned invalid response",
                "quota_error": False,
            }

        if not response.strip():
            return {
                "provider": provider_name,
                "response": None,
                "error": "Provider returned empty response",
                "quota_error": False,
            }

        return {
            "provider": provider_name,
            "response": response,
            "error": None,
            "quota_error": False,
        }
    except Exception as error:
        return {
            "provider": provider_name,
            "response": None,
            "error": str(error),
            "quota_error": is_quota_error(error),
        }


def ask_council(question: str) -> dict:
    gemini_result = _ask_provider("gemini", ask_gemini, question)
    deepseek_result = _ask_provider("deepseek", ask_deepseek, question)

    gemini_response = gemini_result["response"]
    deepseek_response = deepseek_result["response"]

    provider_errors = {
        "gemini": gemini_result["error"],
        "deepseek": deepseek_result["error"],
    }

    quota_errors = {
        "gemini": gemini_result["quota_error"],
        "deepseek": deepseek_result["quota_error"],
    }

    if gemini_response is None and deepseek_response is None:
        raise RuntimeError(
            "Both providers failed: "
            f"gemini={provider_errors['gemini']}; "
            f"deepseek={provider_errors['deepseek']}"
        )

    if gemini_response is None or deepseek_response is None:
        return {
            "question": question,
            "responses": {
                "gemini": gemini_response,
                "deepseek": deepseek_response,
            },
            "provider_errors": provider_errors,
            "quota_errors": quota_errors,
            "status": "degraded",
            "degraded_reason": "provider_failure",
            "judgment": None,
            "judgment_error": None,
            "debate": None,
            "debate_error": None,
        }

    try:
        judgment = run_dual_judgment(
            question=question,
            gemini_response=gemini_response,
            deepseek_response=deepseek_response,
        )
    except Exception as error:
        return {
            "question": question,
            "responses": {
                "gemini": gemini_response,
                "deepseek": deepseek_response,
            },
            "provider_errors": provider_errors,
            "quota_errors": quota_errors,
            "status": "degraded",
            "degraded_reason": "judge_failure",
            "judgment": None,
            "judgment_error": str(error),
            "debate": None,
            "debate_error": None,
        }

    debate = None
    debate_error = None

    if judgment["final_needs_debate"]:
        try:
            debate = run_debate(
                question=question,
                gemini_response=gemini_response,
                deepseek_response=deepseek_response,
            )
        except Exception as error:
            debate_error = str(error)

    status = "degraded" if debate_error else "ok"
    degraded_reason = "debate_failure" if debate_error else None

    return {
        "question": question,
        "responses": {
            "gemini": gemini_response,
            "deepseek": deepseek_response,
        },
        "provider_errors": provider_errors,
        "quota_errors": quota_errors,
        "status": status,
        "degraded_reason": degraded_reason,
        "judgment": judgment,
        "judgment_error": None,
        "debate": debate,
        "debate_error": debate_error,
    }