import inspect

from agent.providers.registry import PROVIDERS


def test_registered_providers_accept_one_required_prompt_argument():
    for provider_name, provider in PROVIDERS.items():
        signature = inspect.signature(provider)
        required_parameters = [
            parameter
            for parameter in signature.parameters.values()
            if parameter.default is inspect.Parameter.empty
        ]

        assert len(required_parameters) == 1, provider_name
        assert required_parameters[0].name == "prompt", provider_name


def test_registered_provider_prompt_argument_is_positional_or_keyword():
    for provider_name, provider in PROVIDERS.items():
        signature = inspect.signature(provider)
        prompt_parameter = signature.parameters["prompt"]

        assert (
            prompt_parameter.kind
            == inspect.Parameter.POSITIONAL_OR_KEYWORD
        ), provider_name