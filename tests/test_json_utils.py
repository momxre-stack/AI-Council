import pytest

from agent.json_utils import parse_json_object


def test_parse_json_object_accepts_clean_json():
    result = parse_json_object('{"answer": "ok"}', "Test")

    assert result == {"answer": "ok"}


def test_parse_json_object_accepts_wrapper_text():
    result = parse_json_object(
        'Here is the result: {"answer": "ok"} Thanks.',
        "Test",
    )

    assert result == {"answer": "ok"}


def test_parse_json_object_accepts_markdown_fenced_json():
    result = parse_json_object(
        """```json
{"answer": "ok"}
```""",
        "Test",
    )

    assert result == {"answer": "ok"}


def test_parse_json_object_raises_when_json_is_missing():
    with pytest.raises(ValueError):
        parse_json_object("No JSON here", "Test")


def test_parse_json_object_raises_when_json_is_malformed():
    with pytest.raises(ValueError):
        parse_json_object('{"answer": "bad "quote""}', "Test")