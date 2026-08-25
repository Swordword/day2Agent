"""W1D4: build two testable prompts for the same product task."""


def build_zero_shot_prompt(requirement: str) -> str:
    """Return a prompt with no worked example.

    The contract must define:
    - the model's role and goal;
    - hard constraints, especially how to handle missing information;
    - the required output sections;
    - observable acceptance criteria.
    """
    # TODO 1: write the zero-shot prompt.
    return f"""
    角色：前端需求分析师
    目标：把自然语言需求拆成可执行的前端任务
    输入：{requirement}
    硬约束：不得编造 API、权限和业务规则；缺失信息列为待确认问题
    输出格式：任务列表、验收标准、待确认问题
    验收标准：任务具体可执行；验收条件可观察；明确覆盖用户需求
    信息不足时：提出问题，不自行补全
    """


def build_few_shot_prompt(requirement: str) -> str:
    """Return the same contract plus one useful input/output example.

    Keep the real requirement visually separate from the example. The example
    should teach a difficult boundary, not merely make the prompt longer.
    """
    return f"""
    你是一名资深前端需求分析师。
    
    目标：
    把用户的自然语言需求拆解成可执行、可验收的前端任务。
    
    硬约束：
    1. 不得编造不存在的 API、权限、数据字段或业务规则。
    2. 需求信息不足时，必须列出待确认问题，不要自行猜测。
    3. 每个任务都要具体到页面、组件或交互行为。
    4. 验收标准必须是用户可以观察和验证的结果。
    
    输出格式：
    任务列表：
    - 任务 1：...
    - 任务 2：...
    
    验收标准：
    - Given ...
    - When ...
    - Then ...
    
    待确认问题：
    - ...
    
    示例输入：
    根据商品列表的供货价进行排序。
    
    示例输出：
    任务列表：
    - 在商品列表页面增加供货价排序选项。
    - 在排序控件中提供“供货价从低到高”和“供货价从高到低”。
    
    验收标准：
    - Given 商品数据包含供货价
    - When 用户选择“供货价从低到高”
    - Then 商品按照供货价升序排列
    
    待确认问题：
    - 当前是否已有返回商品供货价的接口？
    - 供货价为空时应该如何排序？
    
    现在请处理以下真实需求：
    {requirement}
    """
