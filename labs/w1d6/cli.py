"""W1D6：需求澄清 CLI 的纯函数基础。

先把输入校验和上下文合并做成不依赖终端、不依赖模型的纯函数，
后续再把它们接入交互循环和 W1D5 的结构化模型调用。
"""


def validate_requirement(text: str) -> str:
    """校验需求非空，并返回去除首尾空白后的文本。"""
    raise NotImplementedError


def build_final_requirement(
    original: str,
    answers: dict[str, str],
    revision: str = "",
) -> str:
    """合并原始需求、问题答案和用户修改意见。"""
    raise NotImplementedError
