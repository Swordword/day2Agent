"""W1D5: bounded retry around a model that sometimes breaks the contract.

`call_model` is injected so the retry logic can be tested without spending
tokens or depending on the network.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

from labs.w1d5.models import Requirement
from labs.w1d5.parsing import StructuredOutputError, parse_requirement
from labs.w1d5.prompts import build_structured_prompt, response_schema_text

PromptKind = Literal["initial", "repair"]


@dataclass
class Attempt:
    """One model call and what happened to its output."""

    prompt_kind: PromptKind
    raw: str
    error: str | None = None


@dataclass
class RequirementResult:
    """The outcome of a bounded attempt sequence, success or not."""

    requirement: Requirement | None = None
    attempts: list[Attempt] = field(default_factory=list)

    @property
    def succeeded(self) -> bool:
        return self.requirement is not None

    @property
    def error_message(self) -> str | None:
        """Return the last error, for display when every attempt failed."""
        if self.succeeded or not self.attempts:
            return None
        return self.attempts[-1].error


def build_repair_prompt(*, requirement: str, raw: str, error: str) -> str:
    """Return a prompt that asks the model to fix its own broken output.

    It must contain the original requirement, the rejected output and the exact
    error, and repeat that the reply is one JSON object with no fence.
    """
    # TODO 5: write the repair prompt.
    return f"""你需要修复一份未通过校验的结构化输出。

原始需求：
{requirement}

未通过校验的输出：
{raw}

校验错误：
{error}

输出必须符合以下 JSON Schema：
{response_schema_text()}

修复规则：
1. 根据校验错误修复原输出。
2. 不得编造原始需求中没有提供的信息。
3. 缺失信息必须放入 open_questions。
4. 只返回一个完整的 JSON 对象。
5. 不要使用 Markdown 代码围栏。
6. 不要在 JSON 前后添加解释或其他文本。
"""


def request_requirement(
    requirement: str,
    *,
    call_model: Callable[[str], str],
    max_attempts: int = 3,
) -> RequirementResult:
    """Ask the model for a `Requirement`, repairing at most `max_attempts` times.

    Rules:
    - `max_attempts` must be at least 1, otherwise raise ValueError;
    - attempt 1 uses `build_structured_prompt`, later attempts use
      `build_repair_prompt` with the previous raw output and error;
    - every call is recorded in `attempts`, successful or not;
    - a `StructuredOutputError` never escapes: return a failed result instead,
      so the caller can show the error rather than crash;
    - stop as soon as one attempt validates.
    """
    # TODO 6: implement the bounded retry loop.
    # raise NotImplementedError
    if max_attempts < 1:
        raise ValueError("max_attempts 至少为 1")
    attempts: list[Attempt] = []
    last_raw = ""
    last_error = ""

    for i in range(max_attempts):
        prompt_kind: PromptKind = "initial" if i == 0 else "repair"
        if i == 0:
            prompt = build_structured_prompt(requirement)
        else:
            prompt = build_repair_prompt(
                requirement=requirement, 
                raw=last_raw, 
                error=last_error
            )
        raw = call_model(prompt)
        try:
            parsed = parse_requirement(raw)
        except StructuredOutputError as e:
            last_raw = raw
            last_error = str(e)
            attempts.append(Attempt(prompt_kind=prompt_kind, raw=raw, error=last_error))
            continue

        attempts.append(Attempt(prompt_kind=prompt_kind, raw=raw, error=None))
        return RequirementResult(requirement=parsed, attempts=attempts)
    return RequirementResult(requirement=None, attempts=attempts)

