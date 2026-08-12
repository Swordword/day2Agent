"""W1D2 练习 B：带并发限制和超时的异步批量调用模拟器。"""

import asyncio
from dataclasses import dataclass
from time import perf_counter


@dataclass(slots=True)
class CallResult:
    name: str
    status: str
    elapsed_ms: int
    error: str | None = None


async def fake_model_call(name: str, delay: float) -> str:
    """模拟一次 I/O 调用。负延迟代表调用失败。"""
    if delay < 0:
        raise ValueError("delay 不能为负数")
    await asyncio.sleep(delay)
    return f"{name}:ok"


async def run_one(
    name: str,
    delay: float,
    *,
    semaphore: asyncio.Semaphore,
    timeout: float,
) -> CallResult:
    """TODO 1：在信号量内调用 fake_model_call，并处理超时与普通异常。

    status 取值：
    - 成功："ok"
    - 超时："timeout"
    - 其他异常："error"

    elapsed_ms 必须记录每个任务自身的执行耗时。
    """
    async with semaphore:
        started_at = perf_counter()
        try:
            async with asyncio.timeout(timeout):
                await fake_model_call(name, delay)
                status = "ok"
                error = None
        except asyncio.TimeoutError:
            status = "timeout"
            error = None
        except Exception as e:
            status = "error"
            error = str(e)
        elapsed_ms = round((perf_counter() - started_at) * 1000)
    return CallResult(name, status, elapsed_ms, error)
    

async def run_batch(
    jobs: list[tuple[str, float]],
    *,
    max_concurrency: int,
    timeout: float,
) -> list[CallResult]:
    """TODO 2：并发执行全部任务，同时将并发量限制为 max_concurrency。

    要求：
    - max_concurrency 小于 1 时抛出 ValueError；
    - 返回结果顺序与 jobs 输入顺序一致；
    - 一个任务失败不能中断其他任务。
    """
    if max_concurrency < 1:
        raise ValueError("max_concurrency 必须大于 0")

    semaphore = asyncio.Semaphore(max_concurrency)
    
    tasks = [run_one(name, delay, semaphore=semaphore, timeout=timeout) for name, delay in jobs]

    return await asyncio.gather(*tasks)
    


async def main() -> None:
    jobs = [("fast", 0.05), ("slow", 0.3), ("broken", -1), ("normal", 0.1)]
    results = await run_batch(jobs, max_concurrency=2, timeout=0.2)
    for result in results:
        print('result:', result)


if __name__ == "__main__":
    asyncio.run(main())
