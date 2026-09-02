"""W1D5: recover, parse and validate the model's structured answer.

Two failures must be told apart, because they need different fixes:
- the text is not valid JSON (a formatting failure);
- the JSON is valid but does not satisfy the schema (a contract failure).
"""

import json

from pydantic import ValidationError
from labs.w1d5.models import Requirement


class StructuredOutputError(Exception):
    """Raised when model output cannot become a valid `Requirement`.

    The message is shown to the user and fed back to the model, so it must be
    specific: which stage failed and what was wrong.
    """

def extract_json_block(raw: str) -> str:
    """Return the JSON object hidden in `raw` model text.

    Real answers arrive wrapped in ```json fences or padded with commentary,
    so recover the outermost `{...}` block instead of trusting the model.

    Raise `StructuredOutputError` when no candidate block exists at all.
    Do not attempt to repair invalid JSON here; that is the model's job.
    """
    # TODO 3: strip fences/prose and return the outermost JSON object text.
    # raise NotImplementedError
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or start >= end:
        raise StructuredOutputError("未找到 JSON 对象")
    return raw[start : end + 1]



def parse_requirement(raw: str) -> Requirement:
    """Parse and validate `raw` model text into a `Requirement`.

    Raise `StructuredOutputError` for both failure kinds, with a message that
    names the stage ("JSON 解析失败" / "结构校验失败") and includes the
    underlying error detail.
    """
    # TODO 4: extract, json.loads, then Requirement.model_validate.
    # raise NotImplementedError
    block = extract_json_block(raw)
    try:
        data = json.loads(block)
    except json.JSONDecodeError as e:
        raise StructuredOutputError(f"JSON 解析失败：{e}") from e
    try:
        return Requirement.model_validate(data)
    except ValidationError as e:
        raise StructuredOutputError(f"结构校验失败：{e}") from e


