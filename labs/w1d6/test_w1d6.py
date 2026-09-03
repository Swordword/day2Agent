"""W1D6：需求澄清 CLI 纯函数测试。"""

import pytest

from labs.w1d6.cli import build_final_requirement, validate_requirement


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
