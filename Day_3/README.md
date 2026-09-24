# AI Fluency Training — Day 3 Lab Manual

## Overview
This repository documents building a ReAct-style agent loop entirely from scratch, then deliberately comparing an unguarded version against a guarded version to observe real agent failure modes — particularly infinite tool-call loops.

## Files

| File | Description |
|---|---|
| `config.py` | Shared setup — LLM provider, API client |
| `my_tools.py` | Tool registry, including `read_webpage` |
| `my_agent.py` | The bare agent loop with **no guards** — built to demonstrate failure |
| `my_agent_fixed.py` | The same loop with **guards added**: repeat-call detection, tool output size cap, total character budget |
| `notice.html` | A real fee notice the agent successfully reads |
| `fees.html` | Intentionally does not exist — tests safe error handling |
| `big.html` | A large attendance register — used to trigger a repeated-call loop |

## How to run

1. Activate the virtual environment and install dependencies (see `requirements.txt`).
2. Add your own `.env` file with your provider and API key.
3. Run both agents to compare: