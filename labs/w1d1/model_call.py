"""W1D1: minimal, measurable OpenAI Responses API call in Python."""

import os
from time import perf_counter

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("缺少 OPENAI_API_KEY：请先把 .env.example 复制为 .env 并填写密钥。")

    client = OpenAI()
    started_at = perf_counter()
    response = client.responses.create(
        model=model,
        input="用一句话解释：为什么 Agent 的模型调用需要记录耗时和 Token？",
    )
    latency_ms = round((perf_counter() - started_at) * 1000)

    print(response.output_text)
    print(
        {
            "language": "python",
            "model": model,
            "latency_ms": latency_ms,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    )


if __name__ == "__main__":
    main()
