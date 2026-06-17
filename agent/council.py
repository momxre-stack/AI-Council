from agent.providers.gemini import ask_gemini
from agent.providers.deepseek import ask_deepseek
from agent.dual_judge import run_dual_judgment
from agent.debate import run_debate


def _ask_provider(provider_name: str, provider, question: str) -> dict:
    try:
        return {
            "provider": provider_name,
            "response": provider(question),
            "error": None,
        }

    except Exception as error:
        return {
            "provider": provider_name,
            "response": None,
            "error": str(error),
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

    if gemini_response is None and deepseek_response is None:
        raise RuntimeError("Both providers failed")

    if gemini_response is None or deepseek_response is None:
        return {
            "question": question,
            "responses": {
                "gemini": gemini_response,
                "deepseek": deepseek_response,
            },
            "provider_errors": provider_errors,
            "status": "degraded",
            "judgment": None,
            "debate": None,
        }

    judgment = run_dual_judgment(
        question=question,
        gemini_response=gemini_response,
        deepseek_response=deepseek_response,
    )

    debate = None

    if judgment["final_needs_debate"]:
        debate = run_debate(
            question=question,
            gemini_response=gemini_response,
            deepseek_response=deepseek_response,
        )

    return {
        "question": question,
        "responses": {
            "gemini": gemini_response,
            "deepseek": deepseek_response,
        },
        "provider_errors": provider_errors,
        "status": "ok",
        "judgment": judgment,
        "debate": debate,
    }