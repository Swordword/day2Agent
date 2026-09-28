"""W1D6：需求澄清 CLI 的纯函数基础。

先把输入校验和上下文合并做成不依赖终端、不依赖模型的纯函数，
后续再把它们接入交互循环和 W1D5 的结构化模型调用。
"""

from typing import Literal

from labs.w1d5.models import Requirement
from labs.w1d5.pipeline import request_requirement


def validate_requirement(text: str) -> str:
    """校验需求非空，并返回去除首尾空白后的文本。"""
    # raise NotImplementedError
    if text.strip() == "":
        raise ValueError("需求为空")
    return text.strip()


def build_final_requirement(
    original: str,
    answers: dict[str, str],
    revision: str = "",
) -> str:
    """合并原始需求、问题答案和用户修改意见。"""
    parts = [f"原始需求：\n{original.strip()}"]

    answered = [
        f"{question}：{answer.strip()}"
        for question, answer in answers.items()
        if answer.strip()
    ]

    if answered:
        parts.append("补充信息：\n" + "\n".join(answered))

    if revision.strip():
        parts.append("用户修改意见：\n" + revision.strip())

    return "\n\n".join(parts)


NextStep = Literal[
    "collect_answers",
    "request_confirmation",
    "done",
]


def decide_next_step(
    *,
    has_open_questions: bool,
    confirmed: bool,
) -> NextStep:
    """根据待确认问题和用户确认状态决定下一步。"""
    # 先处理待确认问题
    if has_open_questions:
        return "collect_answers"
    # 没有问题后，再判断用户是否确认
    if not confirmed:
        return "request_confirmation"
    return "done"


def format_requirement(requirement: Requirement) -> str:
    """把结构化需求格式化为终端可读文本。"""
    lines = [f"需求摘要：{requirement.summary}"]

    for index, task in enumerate(requirement.tasks, start=1):
        lines.append("")
        lines.append(f"任务 {index}：{task.title}")

        for criterion in task.acceptance_criteria:
            lines.append(f"  验收标准：{criterion.criterion}")

    if requirement.open_questions:
        lines.append("")
        lines.append("待确认问题：")

        for index, question in enumerate(requirement.open_questions, start=1):
            lines.append(f"{index}. {question}")

    return "\n".join(lines)