from agent.providers.deepseek import ask_deepseek
from agent.providers.gemini import ask_gemini


PROVIDERS = {
    "gemini": ask_gemini,
    "deepseek": ask_deepseek,
}