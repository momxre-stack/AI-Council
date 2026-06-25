from agent.providers.deepseek import ask_deepseek
from agent.providers.gemini import ask_gemini
from agent.providers.openai_provider import ask_openai
from agent.providers.registry import PROVIDERS


def test_provider_registry_points_to_gemini_provider():
    assert PROVIDERS["gemini"] is ask_gemini


def test_provider_registry_points_to_deepseek_provider():
    assert PROVIDERS["deepseek"] is ask_deepseek

def test_provider_registry_points_to_openai_provider():
    assert PROVIDERS["openai"] is ask_openai