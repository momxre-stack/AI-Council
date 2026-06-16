from agent.providers.gemini import ask_gemini
from agent.providers.deepseek import ask_deepseek
from agent.analyzer import analyze_responses


def ask_council(question: str) -> dict:
    gemini_response = ask_gemini(question)
    deepseek_response = ask_deepseek(question)

    analysis = analyze_responses(
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
        "analysis": analysis,
    }