# Analysis: Building an Agent from Scratch and Its Failure Modes

## Scenario
A college notice-reading assistant that uses a `read_webpage` tool to answer questions from local HTML files: a fee notice (`notice.html`), a missing file (`fees.html`, intentionally absent to test error handling), and a large attendance register (`big.html`).

## 1. Explanation of the agent loop
The agent follows the standard ReAct-style loop: it sends the conversation to the LLM along with the available tool schemas, checks whether the reply contains a tool call, and if so, runs that tool and appends the result as an observation before looping again. This repeats until the model returns a plain answer with no further tool calls, or a safety limit is reached. Two versions of this loop were built: an unguarded version (`my_agent.py`) implementing only the bare loop, and a guarded version (`my_agent_fixed.py`) adding three defensive checks — repeat-call detection, a maximum characters-per-tool-result cap, and a total character budget for the run.

## 2. Observed failure modes

**Safe tool failure (both versions):** When asked to read `fees.html`, a file that does not exist, both the guarded and unguarded agents correctly reported that the file could not be found, rather than crashing or inventing a fee. This confirms the tool itself returns a readable error string instead of raising an exception, satisfying the defensive-checklist requirement that "every tool returns a readable error message instead of raising an exception."

**Infinite loop (the key difference):** When asked to read `big.html` and count the students, both agents successfully read the file's content on the first call. However, neither agent used that returned content to answer immediately — instead, both re-called `read_webpage` with the identical arguments. The unguarded agent repeated this at least four times before ending with a blank, unhelpful final answer, with no indication to the user of what went wrong. The guarded agent's repeat-detection check recognised that the same tool had been called three times with the same arguments and no progress was being made, and stopped the run with a clear message: *"Stopped: the tool read_webpage was called 3 times with the same arguments and no progress was made."*

## 3. Comparison table

| Basis | Unguarded agent | Guarded agent |
|---|---|---|
| Handles missing file | Yes — safe error message | Yes — safe error message |
| Detects repeated identical tool calls | No | Yes — stops after 3 repeats |
| Behaviour when stuck | Loops silently, ends with a blank answer | Stops cleanly with an explanatory message |
| User-facing outcome when stuck | Confusing — looks like the agent simply failed to answer | Transparent — the user is told exactly what went wrong |
| Bounded tool output size | No | Yes (MAX_TOOL_CHARS) |
| Bounded total run size | No | Yes (CHAR_BUDGET) |

## 4. Why this matters
This test exposes a real limitation of a small model: after successfully reading a large HTML page, the model did not recognise that it already had enough information to answer, and instead repeated the same action. Without a guard, this kind of loop can run indefinitely (up to the loop's outer step limit) or, as observed here, quietly terminate with no useful output — the worst outcome for a real user, since nothing in the response explains that anything went wrong. The repeat-detection guard converts this silent failure into a clear, debuggable one.

## 5. Conclusion
Building the agent loop from scratch, rather than relying on a framework, made it possible to see exactly where and why the failure occurred: the model itself made the mistake of re-fetching data it already had, and only an explicit guard in the surrounding code could catch and correct that behaviour. This confirms the core lesson of Day 3 — agents do not fail by crashing the way ordinary software does; they fail while still running and still appearing to function, which is why guards for infinite loops, unbounded tool output, and unbounded context growth must be designed in from the start rather than added after something goes wrong in production.