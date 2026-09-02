"""W1D5: turn the W1D4 prompt contract into a schema-constrained prompt."""

import json

from labs.w1d5.models import Requirement


def response_schema_text() -> str:
    """Return the JSON schema of `Requirement` as prompt-ready text.

    The schema is generated from the model, never hand-written, so the prompt
    and the parser can never disagree about field names.
    """
    return json.dumps(Requirement.model_json_schema(), ensure_ascii=False, indent=2)


def build_structured_prompt(requirement: str) -> str:
    """Return a prompt that must produce one JSON object and nothing else.

    Keep the W1D4 contract (role, goal, hard constraints, acceptance criteria)
    and add the machine-readable part:
    - the response must be a single JSON object matching `response_schema_text()`;
    - no Markdown fence, no explanation before or after the JSON;
    - missing information goes into `open_questions`, never into invented
      endpoints, fields, permissions or numeric thresholds.
    """
    # TODO 2: write the prompt. It must contain the real requirement and the
    # schema text, so a schema change automatically reaches the prompt.
    # raise NotImplementedError

    return f"""你是一名前端需求分析师。
    请将下面的自然语言需求拆解为可执行的开发任务。
    硬约束：
    1. 只能依据需求中明确提供的信息。
    2. 不得编造 API、字段、权限、业务规则或数字阈值。
    3. 信息不足时，将问题写入 open_questions，不要自行假设。
    4. 每个任务必须包含至少一条可观察、可判定的验收标准。
    5. 只返回一个 JSON 对象。
    6. 不要使用 Markdown 代码围栏。
    7. 不要在 JSON 前后添加解释或其他文本。
    
    输出必须符合以下 JSON Schema：
    {response_schema_text()}

    用户需求：
    {requirement}

    """
