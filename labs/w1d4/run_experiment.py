"""Run the W1D4 prompts and save outputs plus token usage as JSONL."""

import argparse
import json
import os
from pathlib import Path
from time import perf_counter

from dotenv import load_dotenv
from openai import OpenAI

from labs.w1d4.cases import TEST_CASES
from labs.w1d4.prompts import build_few_shot_prompt, build_zero_shot_prompt


BUILDERS = {
    "zero-shot": build_zero_shot_prompt,
    "few-shot": build_few_shot_prompt,
}


def parse_case_numbers(raw: str) -> list[int]:
    numbers = [int(part.strip()) for part in raw.split(",")]
    if not numbers or any(number < 1 or number > len(TEST_CASES) for number in numbers):
        raise argparse.ArgumentTypeError("用例编号必须在 1 到 10 之间")
    return numbers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=parse_case_numbers, default=list(range(1, 11)))
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.repeats < 1:
        raise SystemExit("--repeats 必须大于 0")

    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("缺少 OPENAI_API_KEY")

    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    # A learning experiment must fail visibly instead of waiting indefinitely
    # on one provider request and blocking all later measurements.
    client = OpenAI(timeout=60.0, max_retries=0)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as output_file:
        for prompt_version, builder in BUILDERS.items():
            for case_number in args.cases:
                requirement = TEST_CASES[case_number - 1]
                for run_number in range(1, args.repeats + 1):
                    started_at = perf_counter()
                    response = client.responses.create(
                        model=model,
                        input=builder(requirement),
                    )
                    record = {
                        "prompt_version": prompt_version,
                        "case_number": case_number,
                        "run_number": run_number,
                        "requirement": requirement,
                        "output": response.output_text,
                        "model": model,
                        "latency_ms": round((perf_counter() - started_at) * 1000),
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens,
                    }
                    output_file.write(json.dumps(record, ensure_ascii=False) + "\n")
                    print(
                        f"{prompt_version} case={case_number} run={run_number} "
                        f"tokens={record['input_tokens']}+{record['output_tokens']}"
                    )

    print(f"结果已保存到 {args.output}")


if __name__ == "__main__":
    main()
