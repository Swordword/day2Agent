# Agent 开发 Resources

## Knowledge

- [OpenAI API Quickstart](https://developers.openai.com/api/docs/quickstart)
  Responses API 与 Python、JavaScript SDK 的官方入门。用于：W1D1 的双端最小调用。
- [OpenAI Models](https://developers.openai.com/api/docs/models)
  当前模型能力、上下文与选择建议。用于：选择实验模型并理解质量、延迟、成本取舍。
- [OpenAI Model Guidance](https://developers.openai.com/api/docs/guides/latest-model)
  当前模型家族及 Responses API 的官方实践。用于：后续模型迁移、Prompt 与推理参数实验。
- [Python `time` documentation](https://docs.python.org/3/library/time.html#time.perf_counter)
  单调高精度计时器的官方说明。用于：Python 调用耗时测量。
- [Node.js Performance Measurement APIs](https://nodejs.org/api/perf_hooks.html)
  Node 高精度性能测量 API。用于：TypeScript 调用耗时测量。
- [Python 3.12 `typing`](https://docs.python.org/3.12/library/typing.html)
  Python 类型注解的官方参考。用于：W1D2 类型注解、生成器与协程返回类型。
- [Python 3.12 `asyncio`](https://docs.python.org/3.12/library/asyncio.html)
  Python 异步 I/O 的官方入口。用于：W1D2 并发、超时与任务调度。
- [Python 3.12 `dataclasses`](https://docs.python.org/3.12/library/dataclasses.html)
  标准库数据类的官方说明。用于：对比普通类、dataclass 与 Pydantic。
- [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/)
  `BaseModel`、数据验证、转换和序列化的官方说明。用于：把 TypeScript interface 改写成可运行时验证的 Python 模型。
- [OpenAI Model Guidance](https://developers.openai.com/api/docs/guides/latest-model)
  官方上下文管理与 Token 效率建议。用于：W1D3 理解手动维护历史、精简重复指令和上下文成本。
- [OpenAI Models](https://developers.openai.com/api/docs/models)
  官方模型能力与上下文窗口信息。用于：W1D3 区分模型容量、输入预算和实际用量。
- [OpenAI Model Guidance](https://developers.openai.com/api/docs/guides/latest-model)
  官方 Prompt 最佳实践：保留任务目标、上下文、硬约束和成功标准，并用代表性评测集验证修改。用于：W1D4 Prompt 契约与对照实验。
- [OpenAI Evals](https://platform.openai.com/docs/guides/evals)
  官方评测指南。用于：W1D4 将“感觉更好”改成固定用例、固定标准和可重复运行的比较。

## Wisdom (Communities)

- [OpenAI Developer Community](https://community.openai.com/)
  用于核实真实集成问题、常见失败模式和 SDK 使用经验；课程代码仍以官方文档为准。

## Gaps

- 后续进入 LangChain、LangGraph、MCP 与 DeerFlow 时，再按周补充各项目官方文档和源码入口。
