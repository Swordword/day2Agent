/** W1D1: minimal, measurable OpenAI Responses API call in TypeScript. */

import "dotenv/config";
import OpenAI from "openai";
import { performance } from "node:perf_hooks";

const model = process.env.OPENAI_MODEL ?? "gpt-5.6-luna";

if (!process.env.OPENAI_API_KEY) {
  throw new Error(
    "缺少 OPENAI_API_KEY：请先把 .env.example 复制为 .env 并填写密钥。",
  );
}

const client = new OpenAI();
const startedAt = performance.now();
const response = await client.responses.create({
  model,
  input: "用一句话解释：为什么 Agent 的模型调用需要记录耗时和 Token？",
});
const latencyMs = Math.round(performance.now() - startedAt);

console.log(response.output_text);
console.log({
  language: "typescript",
  model,
  latency_ms: latencyMs,
  input_tokens: response.usage?.input_tokens,
  output_tokens: response.usage?.output_tokens,
  total_tokens: response.usage?.total_tokens,
});
