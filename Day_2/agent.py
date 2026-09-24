"""System 3: an AI agent. LLM + tools + loop."""
import json
import re
from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = (
    "You are a college fee assistant. Never guess a fee: always use get_course_fee. "
    "Use calculator for any arithmetic. Available course codes: CS101, AI202, DS303. "
    "If no tool is needed, answer directly."
)

def run_tool_call(name, arguments, verbose, step):
    clean_name = name.split("<|")[0].strip()
    function = TOOL_FUNCTIONS.get(clean_name)
    result = function(**arguments) if function else f"Unknown tool: {clean_name}"
    if verbose:
        print(f"   step {step}: {clean_name}({arguments}) -> {result}")
    return clean_name, result

def agent(question, max_steps=6, verbose=True):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOLS, temperature=0)
            message = response.choices[0].message
        except Exception as e:
            match = re.search(r"'failed_generation':\s*'(\{.*\})'\}\}", str(e))
            if not match:
                return f"Agent error (could not recover): {e}"
            try:
                call = json.loads(match.group(1))
            except Exception:
                return f"Agent error (could not parse recovery): {e}"
            name, result = run_tool_call(call["name"], call.get("arguments", {}), verbose, step)
            messages.append({"role": "assistant", "content": "",
                              "tool_calls": [{"id": "recovered_call", "type": "function",
                                              "function": {"name": name,
                                                           "arguments": json.dumps(call.get("arguments", {}))}}]})
            messages.append({"role": "tool", "tool_call_id": "recovered_call", "content": result})
            continue

        if not message.tool_calls:
            return message.content.strip()

        messages.append({
            "role": "assistant", "content": message.content or "",
            "tool_calls": [{"id": call.id, "type": "function",
                            "function": {"name": call.function.name,
                                         "arguments": call.function.arguments}}
                           for call in message.tool_calls]})
        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments or "{}")
            _, result = run_tool_call(call.function.name, arguments, verbose, step)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
    return "Stopped: maximum steps reached without a final answer."

if __name__ == "__main__":
    banner("SYSTEM 3: AI AGENT")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", agent(question))
        print("-" * 70)