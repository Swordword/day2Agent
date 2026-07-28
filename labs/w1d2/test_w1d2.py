"""W1D2 自动反馈测试。不要修改本文件来让测试通过。"""

import asyncio
import inspect
from typing import get_type_hints

import pytest
from pydantic import ValidationError

from labs.w1d2.async_batch import run_batch
from labs.w1d2.types_and_models import (
    AgentTask,
    format_model_label,
    task_summaries,
)


def test_function_has_type_annotations() -> None:
    hints = get_type_hints(format_model_label)
    assert hints == {"name": str, "version": int, "return": str}
    assert format_model_label("agent", 2) == "agent@2"


def test_agent_task_accepts_valid_input_and_alias() -> None:
    task = AgentTask(
        id="task-1",
        prompt="分析项目",
        priority=2,
        tools=["search", "read"],
        timeoutMs=5000,
    )
    assert task.timeout_ms == 5000


def test_agent_task_rejects_invalid_values_and_extra_fields() -> None:
    with pytest.raises(ValidationError):
        AgentTask(id="x", prompt="", priority=4, tools=[], unknown=True)


def test_task_summaries_is_generator() -> None:
    task = AgentTask(id="a", prompt="检查类型", priority=1, tools=[])
    result = task_summaries([task])
    assert inspect.isgenerator(result)
    assert list(result) == ["a: 检查类型"]


@pytest.mark.asyncio
async def test_batch_handles_success_timeout_and_error() -> None:
    results = await run_batch(
        [("ok", 0.01), ("late", 0.2), ("bad", -1)],
        max_concurrency=2,
        timeout=0.05,
    )
    assert [result.name for result in results] == ["ok", "late", "bad"]
    assert [result.status for result in results] == ["ok", "timeout", "error"]


@pytest.mark.asyncio
async def test_batch_rejects_invalid_concurrency() -> None:
    with pytest.raises(ValueError):
        await run_batch([], max_concurrency=0, timeout=0.1)


@pytest.mark.asyncio
async def test_batch_really_limits_concurrency() -> None:
    started = asyncio.get_running_loop().time()
    await run_batch(
        [("a", 0.04), ("b", 0.04), ("c", 0.04)],
        max_concurrency=1,
        timeout=0.2,
    )
    elapsed = asyncio.get_running_loop().time() - started
    assert elapsed >= 0.1
