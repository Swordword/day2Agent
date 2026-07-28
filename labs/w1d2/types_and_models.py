"""W1D2 练习 A：类型注解与 Pydantic。

只修改标有 TODO 的位置。先运行测试看失败，再逐项完成。
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


def format_model_label(name, version):
    """TODO 1：补全参数与返回值类型注解，不改变函数行为。"""
    return f"{name}@{version}"


# 对照来源：
#
# interface AgentTask {
#   id: string;
#   prompt: string;
#   priority: 1 | 2 | 3;
#   tools: string[];
#   timeoutMs?: number;
# }


class AgentTask:
    id: str
    prompt: str
    priority: Literal[1, 2, 3]
    tools: list[str]
    timeout_ms: int | None = None


class AgentTask(BaseModel):
    """TODO 2：把上面的 TypeScript interface 改写成 Pydantic 模型。

    约束：
    - 拒绝未声明字段；
    - prompt 长度至少为 1；
    - priority 只能是 1、2、3；
    - tools 是字符串列表；
    - timeout_ms 可省略，默认 None，若提供必须大于 0；
    - 接受外部字段名 timeoutMs，并能用 Python 字段名 timeout_ms 构造。
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    # TODO：在这里定义字段
    pass


def task_summaries(tasks):
    """TODO 3：补全类型注解，并将它改成逐个 yield 摘要的生成器。

    每项格式："{id}: {prompt}"
    """
    raise NotImplementedError
