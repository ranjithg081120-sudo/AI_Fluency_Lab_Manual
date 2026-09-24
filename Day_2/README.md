# AI Fluency Training — Day 2 Lab Manual

## Overview
This repository documents the Day 2 Lab Manual exercise: tracing a ReAct agent's reasoning by hand, then comparing it against a real agent's trace, and measuring the effect of Chain-of-Thought prompting and self-consistency on a small model.

## Scenario
Reuses the Day 1 college fee data: CS101 = Rs. 12,000, AI202 = Rs. 18,000, DS303 = Rs. 15,000.

## Files

| File | Description |
|---|---|
| `config.py` | Shared setup — LLM provider, API client, and the private course fee data (reused from Day 1) |
| `tools.py` | Defines the tools (`get_course_fee`, `calculator`) the agent can use (reused from Day 1) |
| `agent.py` | The ReAct agent from Day 1 — LLM + Tools + Loop (reused, imported by react_trace.py) |
| `react_trace.py` | **Part B** — runs the agent on a multi-step scholarship comparison question, to compare its real tool-call trace against a hand-written paper trace |
| `cot_compare.py` | **Part C** — asks 3 reasoning questions with direct prompting vs Chain-of-Thought prompting, with no tools involved |
| `self_consistency.py` | **Part D** — runs one CoT reasoning question 5 times at temperature 0.8 and reports the majority answer |

## Lab structure
- **Part A** (paper only, no code): manually trace Thought → Action → Observation for the question *"Which is cheaper: CS101+AI202 at 10% off, or all three courses at 25% off?"*
- **Part B**: run `react_trace.py` and compare the agent's real trace against the paper trace from Part A
- **Part C**: run `cot_compare.py` to see how step-by-step prompting changes accuracy on pure reasoning questions
- **Part D**: run `self_consistency.py` to see how repeated sampling at higher temperature can catch occasional reasoning errors

## How to run

1. Create and activate a virtual environment: