import pytest
from pydantic import ValidationError

from labs.w1d3.context_manager import Message, build_request, total_tokens, trim_history


def msg(role: str, content: str, tokens: int) -> Message:
    return Message(role=role, content=content, token_count=tokens)  # type: ignore[arg-type]


def test_message_rejects_unknown_role() -> None:
    with pytest.raises(ValidationError):
        msg("critic", "check this", 2)


def test_total_tokens_sums_measured_counts() -> None:
    messages = [msg("system", "rules", 4), msg("user", "hello", 3)]
    assert total_tokens(messages) == 7


def test_trim_keeps_system_and_newest_messages_in_original_order() -> None:
    messages = [
        msg("system", "Be concise", 3),
        msg("user", "old question", 4),
        msg("assistant", "old answer", 5),
        msg("user", "new question", 4),
        msg("assistant", "new answer", 3),
    ]

    trimmed = trim_history(messages, max_tokens=10)

    print('1111 ')
    print(trimmed)


    assert [item.content for item in trimmed] == [
        "Be concise",
        "new question",
        "new answer",
    ]
    assert total_tokens(trimmed) == 10


def test_trim_does_not_skip_a_newer_message_to_fit_an_older_one() -> None:
    messages = [
        msg("system", "rules", 2),
        msg("user", "small but old", 2),
        msg("assistant", "large and new", 7),
    ]

    trimmed = trim_history(messages, max_tokens=6)

    assert [item.content for item in trimmed] == ["rules"]


def test_trim_rejects_impossible_system_budget() -> None:
    with pytest.raises(ValueError, match="system"):
        trim_history([msg("system", "long rules", 8)], max_tokens=7)


def test_build_request_reserves_output_capacity() -> None:
    messages = [
        msg("system", "rules", 3),
        msg("user", "old", 4),
        msg("assistant", "recent", 5),
    ]

    request = build_request(
        model="demo-model",
        messages=messages,
        max_context_tokens=12,
        reserved_output_tokens=4,
    )

    assert request["input_budget"] == 8
    assert request["input_tokens"] == 8
    assert [item["content"] for item in request["messages"]] == ["rules", "recent"]  # type: ignore[index]


def test_build_request_rejects_non_positive_input_budget() -> None:
    with pytest.raises(ValueError, match="input budget"):
        build_request(
            model="demo-model",
            messages=[msg("system", "rules", 2)],
            max_context_tokens=10,
            reserved_output_tokens=10,
        )
