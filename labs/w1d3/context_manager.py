from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Role = Literal["system", "user", "assistant", "tool"]


class Message(BaseModel):
    """A deliberately small message model for today's context experiment."""

    model_config = ConfigDict(extra="forbid")

    role: Role
    content: str = Field(min_length=1)
    token_count: int = Field(ge=1)


def total_tokens(messages: list[Message]) -> int:
    """Return the measured token total for all supplied messages."""
    # TODO 1: sum each message's token_count.
    return sum(message.token_count for message in messages)


def trim_history(messages: list[Message], max_tokens: int) -> list[Message]:
    """Keep system messages and as many newest non-system messages as fit.

    Rules:
    - max_tokens must be positive;
    - system messages are always kept and retain their original order;
    - newest non-system messages are preferred;
    - returned messages retain their original chronological order;
    - if system messages alone exceed the budget, raise ValueError.
    """
    # TODO 2: validate the budget, reserve space for system messages,
    # then scan non-system history from newest to oldest.
    if max_tokens <= 0:
        raise ValueError("input budget")
    system_messages = [message for message in messages if message.role == "system"]
    system_tokens = total_tokens(system_messages)
    if system_tokens > max_tokens:
        raise ValueError("system")
    other_messages = [message for message in messages if message.role != "system"]
    remain_tokens = max_tokens - system_tokens

    remain_messages = []

    for message in reversed(other_messages):
        if  message.token_count <= remain_tokens:
            remain_messages.append(message)
            remain_tokens -= message.token_count
        else:
            break

    return system_messages + list(reversed(remain_messages))
    # raise NotImplementedError


def build_request(
    *,
    model: str,
    messages: list[Message],
    max_context_tokens: int,
    reserved_output_tokens: int,
) -> dict[str, object]:
    """Build a printable request after reserving room for model output."""
    # TODO 3: input budget = context capacity - reserved output capacity.
    # Validate it, trim history, and return model/messages/budget metadata.
    input_budget = max_context_tokens - reserved_output_tokens
    trimmed_messages = trim_history(messages, input_budget)
    input_tokens = total_tokens(trimmed_messages)
    messages = [message.model_dump() for message in trimmed_messages]

    return {
        "model":model,
        "messages":messages,       # 每个 Message 转成字典
        "input_budget":input_budget,
        "input_tokens":input_tokens,
    }

    # raise NotImplementedError
