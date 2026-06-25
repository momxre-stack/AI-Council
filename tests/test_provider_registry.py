from agent.providers.registry import PROVIDERS


def test_provider_registry_is_not_empty():
    assert PROVIDERS


def test_expected_providers_exist():
    assert "gemini" in PROVIDERS
    assert "deepseek" in PROVIDERS
    assert "openai" in PROVIDERS


def test_provider_names_are_unique():
    names = list(PROVIDERS.keys())

    assert len(names) == len(set(names))


def test_provider_names_are_strings():
    assert all(isinstance(name, str) for name in PROVIDERS)


def test_provider_entries_are_callable():
    assert all(callable(provider) for provider in PROVIDERS.values())