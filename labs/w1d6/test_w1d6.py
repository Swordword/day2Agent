"""W1D6：需求澄清 CLI 纯函数测试。"""

import pytest

from labs.w1d6.cli import (
    build_final_requirement,
    decide_next_step,
    format_requirement,
    validate_requirement,
)
from labs.w1d5.models import Requirement


def test_validate_requirement_removes_outer_whitespace() -> None:
    """需求前后的空白不应影响后续模型调用。"""
    assert validate_requirement("  增加导出按钮  ") == "增加导出按钮"


@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_validate_requirement_rejects_blank_input(text: str) -> None:
    """空需求无法进入需求分析流程。"""
    with pytest.raises(ValueError):
        validate_requirement(text)


def test_build_final_requirement_includes_non_empty_answers() -> None:
    """非空问题答案应进入下一轮模型输入。"""
    result = build_final_requirement(
        "增加导出按钮",
        {"导出格式": "CSV", "接口是否存在": ""},
    )

    assert "原始需求：\n增加导出按钮" in result
    assert "导出格式：CSV" in result
    assert "接口是否存在" not in result


def test_build_final_requirement_includes_revision_when_provided() -> None:
    """用户修改意见应被明确标记，避免与模型问题答案混淆。"""
    result = build_final_requirement(
        "增加导出按钮",
        {},
        revision="按钮放在列表右上角",
    )

    assert "用户修改意见：\n按钮放在列表右上角" in result


def test_build_final_requirement_omits_empty_revision_section() -> None:
    """没有修改意见时不应产生空的段落。"""
    result = build_final_requirement("增加导出按钮", {}, revision="  ")

    assert "用户修改意见" not in result


def test_build_final_requirement_preserves_answer_order() -> None:
    """合并结果应保留字典中的问题顺序，方便用户核对。"""
    result = build_final_requirement(
        "增加导出按钮",
        {"第一个问题": "答案一", "第二个问题": "答案二"},
    )

    assert result.index("第一个问题：答案一") < result.index("第二个问题：答案二")


# --- 状态决策 ---------------------------------------------------------------


@pytest.mark.parametrize("confirmed", [False, True])
def test_open_questions_must_be_answered_before_completion(confirmed: bool) -> None:
    """只要还有待确认问题，就不能直接完成流程。"""
    assert (
        decide_next_step(has_open_questions=True, confirmed=confirmed)
        == "collect_answers"
    )


def test_draft_without_questions_still_requires_confirmation() -> None:
    """没有待确认问题不代表用户已经认可模型草稿。"""
    assert (
        decide_next_step(has_open_questions=False, confirmed=False)
        == "request_confirmation"
    )


def test_confirmed_result_without_questions_is_done() -> None:
    """待确认问题已清空且用户确认后，流程才算完成。"""
    assert decide_next_step(has_open_questions=False, confirmed=True) == "done"


# --- 结果格式化 -------------------------------------------------------------


def test_format_requirement_displays_summary_tasks_and_criteria() -> None:
    """终端结果应展示摘要、任务和每条验收标准。"""
    requirement = Requirement.model_validate(
        {
            "summary": "增加订单导出功能",
            "tasks": [
                {
                    "title": "增加导出按钮",
                    "acceptance_criteria": [
                        {"criterion": "用户点击按钮后可以触发导出"},
                        {"criterion": "导出失败时显示错误提示"},
                    ],
                }
            ],
            "open_questions": ["导出格式是什么？"],
        }
    )

    result = format_requirement(requirement)

    assert "需求摘要：增加订单导出功能" in result
    assert "任务 1：增加导出按钮" in result
    assert "验收标准：用户点击按钮后可以触发导出" in result
    assert "验收标准：导出失败时显示错误提示" in result


def test_format_requirement_displays_open_questions_when_present() -> None:
    """存在待确认问题时，结果应按顺序展示问题。"""
    requirement = Requirement.model_validate(
        {
            "summary": "增加订单导出功能",
            "tasks": [
                {
                    "title": "增加导出按钮",
                    "acceptance_criteria": [
                        {"criterion": "用户可以点击导出按钮"},
                    ],
                }
            ],
            "open_questions": ["导出格式是什么？", "是否需要权限控制？"],
        }
    )

    result = format_requirement(requirement)

    assert "待确认问题：" in result
    assert "1. 导出格式是什么？" in result
    assert "2. 是否需要权限控制？" in result


def test_format_requirement_omits_empty_open_questions_section() -> None:
    """没有待确认问题时，不应输出空的问题标题。"""
    requirement = Requirement.model_validate(
        {
            "summary": "增加订单导出功能",
            "tasks": [
                {
                    "title": "增加导出按钮",
                    "acceptance_criteria": [
                        {"criterion": "用户可以点击导出按钮"},
                    ],
                }
            ],
        }
    )

    result = format_requirement(requirement)

    assert "待确认问题" not in result
