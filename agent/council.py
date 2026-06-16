from agent.providers.gemini import ask_gemini
from agent.providers.deepseek import ask_deepseek


def ask_council(question: str) -> dict:
    return {
        "question": question,
        "responses": {
            "gemini": ask_gemini(question),
            "deepseek": ask_deepseek(question),
        },
    }