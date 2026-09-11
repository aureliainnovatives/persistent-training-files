"""AgentCore Harness client for the AWS Security Agent lab."""

import json
import sys
import uuid
import boto3

from config import AWS_REGION, HARNESS_ARN, DEFAULT_PROMPT, validate_config
from security_tools import execute_tool


def invoke(client, session_id, messages):
    return client.invoke_harness(
        harnessArn=HARNESS_ARN,
        runtimeSessionId=session_id,
        messages=messages,
    )


def parse_stream(response):
    tool = None
    fragments = []

    for event in response["stream"]:
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            if "text" in delta:
                print(delta["text"], end="", flush=True)
            if tool and "toolUse" in delta:
                part = delta["toolUse"].get("input")
                if isinstance(part, str):
                    fragments.append(part)
                elif isinstance(part, dict):
                    tool["input"].update(part)

        if "contentBlockStart" in event:
            start = event["contentBlockStart"].get("start", {})
            if "toolUse" in start:
                t = start["toolUse"]
                tool = {"toolUseId": t.get("toolUseId"), "name": t.get("name"), "input": {}}

        if "toolUse" in event and isinstance(event["toolUse"], dict):
            t = event["toolUse"]
            tool = {"toolUseId": t.get("toolUseId"), "name": t.get("name"),
                    "input": t.get("input", {})}

        if "runtimeClientError" in event:
            raise RuntimeError(event["runtimeClientError"].get("message", "Harness error"))

    if tool and fragments:
        raw = "".join(fragments)
        if raw.strip():
            tool["input"] = json.loads(raw)

    return tool


def run(prompt):
    validate_config()
    client = boto3.client("bedrock-agentcore", region_name=AWS_REGION)
    session_id = str(uuid.uuid4())

    print(f"Session: {session_id}")
    print(f"User: {prompt}\n")
    messages = [{"role": "user", "content": [{"text": prompt}]}]

    for number in range(1, 21):
        print("Harness: ", end="", flush=True)
        response = invoke(client, session_id, messages)
        tool = parse_stream(response)

        if not tool:
            print()
            return

        name = tool["name"]
        arguments = tool.get("input") or {}
        tool_use_id = tool["toolUseId"]

        print("\n\n" + "=" * 72)
        print(f"INLINE SECURITY TOOL REQUEST #{number}")
        print(f"Function: {name}")
        print(json.dumps(arguments, indent=2))

        result = execute_tool(name, arguments)

        print("\nLOCAL SECURITY TOOL RESULT:")
        print(json.dumps(result, indent=2))
        print("=" * 72 + "\n")

        messages = [
            {"role": "assistant", "content": [{
                "toolUse": {"toolUseId": tool_use_id, "name": name, "input": arguments}
            }]},
            {"role": "user", "content": [{
                "toolResult": {
                    "toolUseId": tool_use_id,
                    "content": [{"text": json.dumps(result)}],
                    "status": "success"
                }
            }]}
        ]

    raise RuntimeError("Maximum tool iterations exceeded.")


if __name__ == "__main__":
    run(" ".join(sys.argv[1:]).strip() or DEFAULT_PROMPT)
