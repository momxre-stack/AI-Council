from agent.providers.deepseek import ask_deepseek
from agent.providers.gemini import ask_gemini
from agent.providers.openai_provider import ask_openai


PROVIDERS = {
    "gemini": ask_gemini,
    "deepseek": ask_deepseek,
    "openai": ask_openai,
}