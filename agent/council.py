from agent.providers.gemini import ask_gemini
from agent.providers.deepseek import ask_deepseek
from agent.judge_v2 import judge_responses_v2


def ask_council(question: str) -> dict:
    gemini_response = ask_gemini(question)
    deepseek_response = ask_deepseek(question)

    judgment = judge_responses_v2(
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
        "judgment": judgment,
    }