import pytest

from labs.w1d4.cases import TEST_CASES
from labs.w1d4.prompts import build_few_shot_prompt, build_zero_shot_prompt


@pytest.mark.parametrize(
    "builder",
    [build_zero_shot_prompt, build_few_shot_prompt],
)
def test_prompt_contains_the_real_requirement(builder) -> None:
    requirement = "用户可以撤销刚删除的任务"
    assert requirement in builder(requirement)


@pytest.mark.parametrize(
    "builder",
    [build_zero_shot_prompt, build_few_shot_prompt],
)
def test_prompt_defines_a_testable_contract(builder) -> None:
    prompt = builder("增加搜索功能")

    for contract_part in ["约束", "输出格式", "验收标准", "待确认问题"]:
        assert contract_part in prompt


def test_zero_shot_does_not_contain_a_worked_example() -> None:
    assert "示例输入" not in build_zero_shot_prompt("增加搜索功能")


def test_few_shot_contains_one_worked_example() -> None:
    prompt = build_few_shot_prompt("增加搜索功能")
    assert prompt.count("示例输入") == 1
    assert prompt.count("示例输出") == 1


def test_there_are_ten_representative_cases() -> None:
    assert len(TEST_CASES) == 10
    assert len(set(TEST_CASES)) == 10
