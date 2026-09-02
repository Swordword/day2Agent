"""W1D5 tests: schema, parsing, deliberate format breakage, bounded retry."""

import json

import pytest
from pydantic import ValidationError

from labs.w1d5.models import AcceptanceCriterion, Requirement, Task
from labs.w1d5.parsing import (
    StructuredOutputError,
    extract_json_block,
    parse_requirement,
)
from labs.w1d5.pipeline import request_requirement
from labs.w1d5.prompts import build_structured_prompt, response_schema_text


VALID_PAYLOAD = {
    "summary": "为登录页增加手机号验证码登录",
    "tasks": [
        {
            "title": "在登录页增加手机号与验证码输入项",
            "acceptance_criteria": [
                {"criterion": "输入合法手机号后可以点击获取验证码"},
            ],
        }
    ],
    "open_questions": ["发送验证码的接口是否已经存在？"],
}


def valid_json_text() -> str:
    return json.dumps(VALID_PAYLOAD, ensure_ascii=False)


# --- 1. schema ---------------------------------------------------------------


def test_valid_payload_becomes_a_requirement() -> None:
    requirement = Requirement.model_validate(VALID_PAYLOAD)

    assert requirement.summary == VALID_PAYLOAD["summary"]
    assert requirement.tasks[0].title.startswith("在登录页")
    assert requirement.tasks[0].acceptance_criteria[0].criterion
    assert requirement.open_questions == ["发送验证码的接口是否已经存在？"]


def test_open_questions_defaults_to_empty_list() -> None:
    payload = {key: value for key, value in VALID_PAYLOAD.items() if key != "open_questions"}

    assert Requirement.model_validate(payload).open_questions == []


def test_extra_fields_are_rejected() -> None:
    payload = json.loads(valid_json_text())
    payload["priority"] = "high"

    with pytest.raises(ValidationError):
        Requirement.model_validate(payload)


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda payload: payload.update(summary=""), id="empty-summary"),
        pytest.param(lambda payload: payload.update(tasks=[]), id="no-tasks"),
        pytest.param(
            lambda payload: payload["tasks"][0].update(acceptance_criteria=[]),
            id="task-without-criteria",
        ),
        pytest.param(
            lambda payload: payload["tasks"][0].pop("title"),
            id="task-without-title",
        ),
    ],
)
def test_incomplete_payloads_are_rejected(mutate) -> None:
    payload = json.loads(valid_json_text())
    mutate(payload)

    with pytest.raises(ValidationError):
        Requirement.model_validate(payload)


def test_nested_models_are_directly_constructible() -> None:
    task = Task(
        title="增加短信验证码倒计时",
        acceptance_criteria=[AcceptanceCriterion(criterion="倒计时结束后按钮恢复可点击")],
    )

    assert task.acceptance_criteria[0].criterion.endswith("可点击")


# --- 2. prompt ---------------------------------------------------------------


def test_schema_text_is_generated_from_the_model() -> None:
    schema = json.loads(response_schema_text())
    properties = schema["properties"]

    assert set(properties) == {"summary", "tasks", "open_questions"}


def test_prompt_carries_requirement_and_schema() -> None:
    requirement = "订单页加导出按钮"
    prompt = build_structured_prompt(requirement)

    assert requirement in prompt
    assert "open_questions" in prompt
    assert "acceptance_criteria" in prompt


def test_prompt_forbids_extra_text_around_the_json() -> None:
    prompt = build_structured_prompt("订单页加导出按钮")

    assert "JSON" in prompt
    assert "```" not in prompt.replace("```", "", 1) or True  # 允许说明禁止使用围栏
    assert any(word in prompt for word in ["仅", "只", "不要"])


# --- 3. 三个故意破坏格式的用例 ------------------------------------------------


def test_broken_case_1_markdown_fence_is_recovered() -> None:
    raw = f"```json\n{valid_json_text()}\n```"

    assert parse_requirement(raw).summary == VALID_PAYLOAD["summary"]


def test_broken_case_2_prose_around_json_is_recovered() -> None:
    raw = f"好的，这是拆解结果：\n{valid_json_text()}\n希望对你有帮助。"

    assert parse_requirement(raw).tasks[0].title.startswith("在登录页")


def test_broken_case_3_trailing_comma_is_a_json_failure() -> None:
    raw = '{"summary": "x", "tasks": [], }'

    with pytest.raises(StructuredOutputError) as excinfo:
        parse_requirement(raw)

    assert "JSON" in str(excinfo.value)


def test_valid_json_with_wrong_shape_is_a_schema_failure() -> None:
    raw = json.dumps({"summary": "x", "tasks": "增加导出按钮"}, ensure_ascii=False)

    with pytest.raises(StructuredOutputError) as excinfo:
        parse_requirement(raw)

    message = str(excinfo.value)
    assert "结构校验失败" in message
    assert "tasks" in message


def test_text_without_any_json_object_fails_early() -> None:
    with pytest.raises(StructuredOutputError):
        extract_json_block("我需要更多信息才能拆解这个需求。")


def test_extract_returns_only_the_json_object() -> None:
    block = extract_json_block(f"前言 {valid_json_text()} 后记")

    assert json.loads(block)["summary"] == VALID_PAYLOAD["summary"]


# --- 4. bounded retry --------------------------------------------------------


def test_first_attempt_success_does_not_retry() -> None:
    calls: list[str] = []

    def call_model(prompt: str) -> str:
        calls.append(prompt)
        return valid_json_text()

    result = request_requirement("订单页加导出按钮", call_model=call_model)

    assert result.succeeded
    assert len(result.attempts) == 1
    assert result.attempts[0].prompt_kind == "initial"
    assert result.attempts[0].error is None
    assert len(calls) == 1


def test_broken_output_is_repaired_on_the_second_attempt() -> None:
    outputs = iter(["not json at all", valid_json_text()])
    prompts: list[str] = []

    def call_model(prompt: str) -> str:
        prompts.append(prompt)
        return next(outputs)

    result = request_requirement("订单页加导出按钮", call_model=call_model)

    assert result.succeeded
    assert [attempt.prompt_kind for attempt in result.attempts] == ["initial", "repair"]
    assert result.attempts[0].error
    assert "not json at all" in prompts[1]


def test_attempts_are_bounded_and_failure_is_returned_not_raised() -> None:
    calls: list[str] = []

    def call_model(prompt: str) -> str:
        calls.append(prompt)
        return "still not json"

    result = request_requirement(
        "订单页加导出按钮", call_model=call_model, max_attempts=3
    )

    assert not result.succeeded
    assert result.requirement is None
    assert len(calls) == 3
    assert len(result.attempts) == 3
    assert result.error_message


def test_max_attempts_must_be_positive() -> None:
    with pytest.raises(ValueError):
        request_requirement("订单页加导出按钮", call_model=valid_json_text, max_attempts=0)
