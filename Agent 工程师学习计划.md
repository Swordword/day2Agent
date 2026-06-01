# Agent 工程师学习计划

> **当前进度**：2026-06-01，推进到 **第 3 天（D 3）**。
> **今日主题**：LLM 原理速览。
> **今日完成标准**：能用自己的话解释 Token、temperature、top-p、上下文窗口、function calling，并写进今日打卡。

> **目标**：6 周内从前端开发工程师转型为初级到中级的 Agent 开发工程师，掌握 LangChain / LangGraph / Qdrant 等核心工具，能独立设计并实现一个具备多智能体协同、Graph RAG、四层记忆体系、Prompt 工程闭环的企业级 Agent 案例。
>
> **每周投入**：周一至周六 ≈ 4 小时/天，周日休整与复盘 ≈ 2 小时（共 ≈ 26 h/周）。
>  **总课时**：约 156 小时 + 1 个完整项目。
>  **节奏单位**：番茄钟（25 分钟学 / 5 分钟休 × 4，再大休 15 分钟）。

------

## 0. 总览（路线图）

| 周次 | 主题                                      | 对应岗位能力              | 阶段产出                  |
| ---- | ----------------------------------------- | ------------------------- | ------------------------- |
| W 1  | Python 速成 + LLM/Prompt 基础             | Prompt Engineering 全链路 | Prompt 库 v 0.1           |
| W 2  | LangChain 核心（Model/Tool/Chain/Memory） | Agent Loop·工具调用       | CLI 单 Agent Demo         |
| W 3  | LangGraph + Agent Loop 工程化             | 任务规划·多轮对话·CoT     | StateGraph 版 ReAct Agent |
| W 4  | 向量检索 + Qdrant + Graph RAG             | Graph RAG·意图识别·置信度 | 企业知识库 RAG 服务       |
| W 5  | 多智能体协同 + 四层记忆体系               | 多 Agent 调度·记忆进化    | Supervisor + Worker 框架  |
| W 6  | 综合实战：企业级招聘 Copilot              | 端到端落地·评测·部署      | 完整项目 + 技术 PPT       |

> 选择"招聘 Copilot"作为综合案例，正好覆盖你工作中提到的"直聘核心算法"场景，可演示岗位 JD 解析、候选人匹配、多轮面试官 Agent、知识库引用、面试纪要总结等完整流程。

------

## 1. 学习方法约定

### 1.1 每日 4 小时模板（推荐）

| 时段          | 内容                  | 说明                                     |
| ------------- | --------------------- | ---------------------------------------- |
| 19:30 - 20:20 | 番茄 1（理论）        | 看官方文档 / 视频，**禁止开 IDE 直接写** |
| 20:20 - 20:30 | 休息                  | 站起来走动、喝水，不刷手机               |
| 20:30 - 21:20 | 番茄 2（敲代码）      | 跟着文档手敲，运行通过即可               |
| 21:20 - 21:35 | 大休 15 分钟          | 远眺、拉伸                               |
| 21:35 - 22:25 | 番茄 3（改造）        | 把示例改成自己的业务，强制偏离           |
| 22:25 - 22:35 | 休息                  |                                          |
| 22:35 - 23:25 | 番茄 4（笔记 + 提问） | Anki 卡片 / 飞书文档 / 准备明天问题      |

### 1.2 每周休整

- **周六晚** 不学新内容，只做"周作业"（见第 3 节）。
- **周日上午** 复盘：用 30 分钟手写本周脑图；下午自由。
- 每周保证 **2 天不超过晚上 11 点**，保护睡眠。

### 1.3 学习方式硬约束

1. **不复制粘贴代码**：任何示例必须手敲一遍。
2. **每个新概念必须能用一句话解释给非 AI 同事听**（写在 README 中）。
3. **每天最后 10 分钟**：写 3 个"明天要查清楚的问题"。
4. **作业必须能跑通 + 截图**，否则视为未完成。

------

## 2. 周度详细任务

### Week 1 · Python 速成 + LLM / Prompt 基础

**目标**：补齐 Python，理解 LLM 工作机制，掌握 Prompt 设计的"工程化"思维（不是写文案）。

#### 2.1 学习任务（按日）

| Day    | 主题                                               | 任务                                                         | 参考                                                         |
| ------ | -------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| D 1 一 | [Python 与前端的差异](Python 与前端的差异)         | uv / venv 环境、类型注解、async / await、dataclass、pydantic v 2 | [pydantic 官方文档](https://docs.pydantic.dev/latest/)       |
| D 2 二 | [Jupyter + dotenv + 调试](Jupyter + dotenv + 调试) | 跑通 `openai` / `anthropic` SDK 的 chat completion，输出 token 用量 | [openai-python](https://github.com/openai/openai-python)     |
| D 3 三 | **今天：LLM 原理速览**                             | Token、温度、Top-p、上下文窗口、function calling 协议        | [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) |
| D 4 四 | Prompt 全链路①：系统提示 + 角色人设                | 写 3 个角色提示词（招聘官 / 法务 / 数据分析师），对比效果    | 同上                                                         |
| D 5 五 | Prompt 全链路②：工具描述 + 不确定性                | 让模型输出 JSON Schema 校验过的结果；强制返回 confidence 字段 | [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) |
| D 6 六 | Prompt 全链路③：CoT 与迭代                         | Few-shot、Chain-of-Thought、Self-Consistency、Reflection 实验 | 论文：*Chain-of-Thought Prompting*                           |
| D 7 日 | 复盘 + 周作业                                      | 见 §3.1                                                      |                                                              |

#### 2.2 强制掌握的概念清单（自检）

- 能解释 `system` / `user` / `assistant` / `tool` 四种消息角色
- 知道 `temperature=0` 不等于 deterministic，能说出原因
- 能区分 Zero-shot / Few-shot / CoT / ReAct
- 能用 pydantic 定义一个工具的入参出参 Schema
- 知道"工具描述写不好 = 工具不存在"

------

### Week 2 · LangChain 核心

**目标**：吃透 LangChain 现代 API（v 0.3+），不要陷在已废弃的 `LLMChain` 里。

#### 2.3 学习任务（按日）

| Day     | 主题                                         | 任务                                                         |
| ------- | -------------------------------------------- | ------------------------------------------------------------ |
| D 8 一  | LCEL（LangChain Expression Language）        | 用 `prompt \| llm \| parser` 拼出 5 个最小可用链             |
| D 9 二  | Tool / @tool 装饰器                          | 写 3 个自定义工具：`search_resume` / `get_jd` / `score_candidate` |
| D 10 三 | `create_agent`（取代旧 AgentExecutor）       | 实现一个 ReAct 风格 Agent，能调上述 3 个工具                 |
| D 11 四 | Streaming + Callback                         | 实现流式输出 + token 计数 + 时延埋点                         |
| D 12 五 | Memory（短期）：`InMemoryChatMessageHistory` | 实现"会话级"记忆，确认它和 Agent Loop 的衔接                 |
| D 13 六 | LangSmith 接入                               | 把 Trace 跑出来，看清楚每一次 Tool 调用的输入输出            |
| D 14 日 | 复盘 + 周作业                                | 见 §3.2                                                      |

#### 2.4 关键 API 对照表

| 旧（不要用）                         | 新（用这个）                                                |
| ------------------------------------ | ----------------------------------------------------------- |
| `LLMChain`                           | `prompt \| llm \| parser` (LCEL)                            |
| `AgentExecutor.from_agent_and_tools` | `create_agent(model, tools, ...)`                           |
| `ConversationBufferMemory`           | `InMemoryChatMessageHistory` + `RunnableWithMessageHistory` |
| `initialize_agent`                   | `langgraph.prebuilt.create_react_agent`                     |

> 配合 `langchain-fundamentals` skill 一起学，避免被过时教程带偏。

------

### Week 3 · LangGraph + Agent Loop 工程化

**目标**：从"Agent 是个黑盒"升级为"Agent 是一张可控的状态图"，能自己设计任务规划与多轮对话循环。

#### 2.5 学习任务（按日）

| Day     | 主题                           | 任务                                                         |
| ------- | ------------------------------ | ------------------------------------------------------------ |
| D 15 一 | StateGraph 基础                | 手画一张 Agent Loop 流程图（planner → tool → reflect → answer） |
| D 16 二 | State / Reducer / TypedDict    | 自己定义 `AgentState`，搞清楚 `Annotated[list, add_messages]` |
| D 17 三 | 条件边 + Command               | 实现"模型决定调工具还是结束"的路由                           |
| D 18 四 | Checkpointer + thread_id       | 持久化对话，重启进程后还能续聊                               |
| D 19 五 | Human-in-the-Loop              | 用 `interrupt()` 让 Agent 在敏感动作前等待人工审批           |
| D 20 六 | Streaming（节点级 / token 级） | 前端展示中间过程而不是黑盒等待                               |
| D 21 日 | 复盘 + 周作业                  | 见 §3.3                                                      |

#### 2.6 必做的图

> 在 `~/study/AI/Agent/diagrams/` 里画 3 张图，markdown 或 mermaid 都可以：
>
> 1. **Agent Loop 状态机**（节点 + 条件边）
> 2. **CoT 决策树**（什么时候走 reflect、什么时候直接 answer）
> 3. **置信度评估流程**（低置信度 → 调工具 / 转人工）

------

### Week 4 · 向量检索 + Qdrant + Graph RAG

**目标**：理解检索增强从"向量近邻"到"图关系推理"的演进路径。

#### 2.7 学习任务（按日）

| Day     | 主题                  | 任务                                                         |
| ------- | --------------------- | ------------------------------------------------------------ |
| D 22 一 | Embedding 原理        | OpenAI / bge / m 3 e 嵌入对比，写一个相似度计算脚本          |
| D 23 二 | Qdrant 入门           | Docker 起一个本地 Qdrant，建 collection、写入、查询          |
| D 24 三 | 文档切分策略          | `RecursiveCharacterTextSplitter`、按语义切、按 Markdown 标题切的对比 |
| D 25 四 | 经典 RAG              | 实现"上传简历 PDF → 问答"，**记录召回率指标**                |
| D 26 五 | 意图识别 + Query 改写 | 用 LLM 做 query 分类 → 路由到不同 collection / KG            |
| D 27 六 | Graph RAG             | 用 Neo 4 j 或 NetworkX 跑一个 mini Graph RAG（实体抽取 → 关系建图 → 子图召回 → 生成） |
| D 28 日 | 复盘 + 周作业         | 见 §3.4                                                      |

#### 2.8 置信度评估的 3 种工程做法

1. **检索端**：top-1 相似度分数 + top-1 与 top-2 的差值。
2. **生成端**：让模型自评 `confidence: 0~1`，配 calibration 检查。
3. **一致性端**：Self-Consistency 多次采样投票，方差越小置信越高。

> 这三种都要在 RAG 服务里实现一次。

------

### Week 5 · 多智能体协同 + 四层记忆体系

**目标**：从单 Agent 升级为多 Agent 系统，并搞清楚记忆"四层"的边界与存储介质。

#### 2.9 学习任务（按日）

| Day     | 主题                                             | 任务                                                         |
| ------- | ------------------------------------------------ | ------------------------------------------------------------ |
| D 29 一 | 多 Agent 拓扑：Supervisor / Swarm / Hierarchical | 读 LangGraph 官方 multi-agent 文档，画 3 种拓扑差异          |
| D 30 二 | Supervisor 模式实现                              | 1 个 Supervisor + 3 个 Worker（JD 解析 / 简历匹配 / 面试官） |
| D 31 三 | 并行调度 + 结果聚合                              | 用 `Send` 把同一任务拆给多个 Worker 并行跑，再聚合           |
| D 32 四 | 会话记忆 + 用户记忆                              | 会话级用 LangGraph checkpointer；用户级用 Store（按 user_id 命名空间） |
| D 33 五 | 角色记忆 + 长期记忆                              | 角色：人设/语气/工具集；长期：向量库 + 摘要 + 反思           |
| D 34 六 | 记忆"进化闭环"                                   | 实现"对话结束 → 提炼 → 写回长期记忆"的后台 Job               |
| D 35 日 | 复盘 + 周作业                                    | 见 §3.5                                                      |

#### 2.10 四层记忆体系参考设计

| 层级              | 存储介质                                 | TTL               | 写入时机           | 例子                   |
| ----------------- | ---------------------------------------- | ----------------- | ------------------ | ---------------------- |
| 会话（Session）   | LangGraph Checkpointer (SQLite/Postgres) | 1~7 天            | 每轮自动           | 当前对话 messages      |
| 用户（User）      | LangGraph Store / Redis                  | 永久（可遗忘）    | 显式声明事实时     | 候选人偏好、简历版本   |
| 角色（Persona）   | YAML / DB 配置                           | 永久              | 配置发布时         | 招聘官人设、工具白名单 |
| 长期（Long-term） | Qdrant + 摘要表                          | 永久 + 周期性回写 | 每次对话结束的反思 | 跨用户的通用经验、FAQ  |

> 这张表直接抄进项目 README，面试可问可答。

------

### Week 6 · 综合实战：企业级招聘 Copilot

**目标**：把前 5 周所学拧成一个完整项目，能跑、能演示、能讲。

#### 2.11 项目需求（最小可用版）

> **场景**：HR 提交一个 JD，系统自动从候选池中筛选并发起初轮面试，最后给出录用建议。

**功能**：

1. JD 上传与解析（结构化抽取：岗位、必备技能、加分项、薪资范围）。
2. 候选简历入库 + Graph RAG 检索（实体：技能/公司/项目，关系：用过/就职于/参与了）。
3. 多 Agent：
   - `Supervisor`：总调度
   - `JDAgent`：解析 JD
   - `MatchAgent`：候选人召回 + 打分（带置信度）
   - `InterviewerAgent`：多轮模拟面试
   - `SummaryAgent`：纪要 + 录用建议
4. 四层记忆全部落地：会话/用户/角色/长期。
5. 人工审批：高风险动作（如自动发拒信）必须 HITL。
6. LangSmith 全链路追踪 + Eval Set。

#### 2.12 按日拆解

| Day     | 任务                                                         |
| ------- | ------------------------------------------------------------ |
| D 36 一 | 工程脚手架：FastAPI + LangGraph + Qdrant + Postgres + Docker Compose |
| D 37 二 | 数据准备：造 50 份假简历 + 5 份真实 JD（脱敏）               |
| D 38 三 | 实现 JDAgent + MatchAgent（含 Graph RAG 子图召回）           |
| D 39 四 | 实现 InterviewerAgent + SummaryAgent，跑通端到端             |
| D 40 五 | 四层记忆全部接好；HITL 接好审批 UI（命令行版即可）           |
| D 41 六 | Eval：搭 20 条评测样例，跑通过率 + 置信度校准曲线            |
| D 42 日 | 录 5 分钟 Demo 视频 + 写 PPT，并把项目放到 GitHub            |

#### 2.13 项目目录建议

```
recruit-copilot/
├── README.md                  # 含架构图 + 四层记忆表 + Eval 结果
├── docker-compose.yml
├── pyproject.toml
├── app/
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── jd_agent.py
│   │   ├── match_agent.py
│   │   ├── interviewer_agent.py
│   │   └── summary_agent.py
│   ├── memory/
│   │   ├── session.py         # checkpointer
│   │   ├── user.py            # store
│   │   ├── persona.py         # yaml loader
│   │   └── longterm.py        # qdrant + reflection
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── graph.py           # 实体关系建图
│   │   └── retriever.py       # 子图召回 + 置信度
│   ├── prompts/               # 所有 prompt 单文件存储，版本化
│   ├── tools/
│   └── api/                   # FastAPI 路由
├── eval/
│   ├── dataset.jsonl
│   └── run.py
└── docs/
    └── architecture.md
```

------

## 3. 阶段作业（必交）

> 每周作业都要：① 跑通 ② 提交到自己的 GitHub ③ README 写清"为什么这么做"。

### 3.1 W 1 作业 · Prompt Library v 0.1

- 至少 10 个 prompt，每个包含：`system / few-shot / user / 输出 Schema / 置信度字段`。
- 用脚本批量回归这 10 个 prompt，给出"格式合规率 / 平均时延 / 平均 token"三个指标。
- **加分项**：写一个简单的 prompt diff 工具，对比改前改后的指标。

### 3.2 W 2 作业 · 简历筛选 CLI Agent

- 输入：JD 文本 + 一个简历文件夹。
- 输出：Top 5 候选人 + 每人一句话理由 + confidence。
- 必须包含：≥ 3 个 tool / 流式输出 / LangSmith trace 截图。

### 3.3 W 3 作业 · 把 W 2 重构为 LangGraph 版

- 用 `StateGraph` 显式建图，至少 4 个节点 + 1 条条件边。
- 加入 `interrupt()`：当 confidence < 0.6 时暂停等待人工选择。
- 实现 checkpointer，演示"杀掉进程再启动还能续上"。

### 3.4 W 4 作业 · 企业知识库 RAG 服务

- 数据：你自己工作中能脱敏的 30 页文档（产品手册、接口文档都行）。
- 必须有：意图分类 → 路由 → Graph RAG / 向量 RAG / 直答三条分支。
- 评测：≥ 30 条 Q&A，给出召回 Top-3 命中率 + 答案合格率。

### 3.5 W 5 作业 · 多 Agent + 四层记忆 Demo

- 至少 1 个 Supervisor + 2 个 Worker，并行执行可观测。
- 四层记忆全部能 dump 出来看到内容。
- 演示一次"长期记忆进化"：第二次对话能用上第一次提炼的事实。

### 3.6 W 6 终极作业 · 招聘 Copilot

- 满足 §2.11 全部功能。

- 交付：① GitHub repo（含 README 架构图）② 5 分钟 Demo 视频 ③ 10 页 PPT ④ Eval 报告。

- 写一篇技术博客

  （≥ 3000 字），主题任选其一：

  - 《我是如何用 LangGraph 设计一个生产级 Agent Loop 的》
  - 《四层记忆体系在招聘场景的落地与坑》
  - 《从向量 RAG 到 Graph RAG：召回率提升 30% 的工程实践》

------

## 4. 推荐资料清单（精选，不贪多）

### 4.1 必读文档

- LangChain v 0.3：https://python.langchain.com/docs/introduction/
- LangGraph：https://langchain-ai.github.io/langgraph/
- Qdrant：https://qdrant.tech/documentation/
- Anthropic Prompt Engineering：https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

### 4.2 必读论文（每篇 1 小时读法：摘要 + 图 + 结论）

- *ReAct: Synergizing Reasoning and Acting in Language Models*
- *Chain-of-Thought Prompting Elicits Reasoning*
- *Self-Consistency Improves CoT*
- *Reflexion: Language Agents with Verbal Reinforcement Learning*
- *Graph RAG* (Microsoft Research, 2024)

### 4.3 视频（选看，不超过 8 小时）

- LangChain 官方 YouTube "LangGraph 101" 系列
- DeepLearning. AI 的 *AI Agents in LangGraph* 短课

### 4.4 你已经具备的优势

- **前端思维**：状态管理（Redux/MobX）与 LangGraph 的 State/Reducer 几乎同构，你比纯后端转过来的人更容易接受。
- **TypeScript / Schema 经验**：直接迁移到 pydantic + Structured Outputs。
- **联调经验**：debug Agent 的 tool 调用本质就是 debug 接口。

------

## 5. 学习反指南（避坑）

1. **不要**一开始就追新模型/新框架（GPT-5? Agent OS?），先把一套主流栈做透。
2. **不要**只跑别人的 notebook，必须改成自己的业务才算学过。
3. **不要**把 Prompt 写在代码字符串里，**从第一天就独立成文件 + 版本号**。
4. **不要**忽略 Eval，没有 Eval 的 Agent 都是玄学。
5. **不要**把"会用 LangChain"当目标，**要把"能设计 Agent 系统"当目标**。

------

## 6. 验收 checklist（6 周结束自测）

> 全部打勾意味着你具备初级到中级 Agent 工程师的能力。

- 能从 0 设计一个 Agent Loop 状态机，并解释每个节点的职责
- 能写出生产可用的 Prompt（含系统提示、工具描述、不确定性、版本）
- 能落地多 Agent Supervisor + 并行 Worker + 结果聚合
- 能区分意图识别 / 向量 RAG / Graph RAG 的适用边界
- 能解释 CoT、Self-Consistency、Reflection 各自解决什么问题
- 能在工程上实现至少两种置信度评估方法
- 能搭建四层记忆体系并演示"记忆进化"
- 能用 LangSmith 调试一次失败的 trace 并修复
- 能产出一个能跑、能演示、能讲清楚的端到端项目
- 能给非技术同事用 5 分钟讲清楚你做的 Agent 是什么

------

## 7. 每日打卡模板（建议复制到飞书 / Notion 用）

```
日期：YYYY-MM-DD（第 N 天 / 共 42 天）
今日主题：
学习时长：____ 番茄钟
代码产出：仓库 / 文件 / commit
关键概念（一句话解释）：
卡住的问题（明天解决）：
对应作业进度：____%
体力 / 注意力评分：1 ~ 5
```

------

> **最后一条**：转型不是冲刺是节奏。计划是地图，但不要把地图当成路。如果某周明显跟不上，**砍内容，不砍节奏**——保留每日 4 番茄、保留周作业，宁可少学一个特性，也不要中断习惯。
