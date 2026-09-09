import json
import uuid
import boto3
from config import REGION, HARNESS_ARN
from cloudops_tools import execute_tool

class HarnessClient:
    def __init__(self):
        self.client = boto3.client("bedrock-agentcore", region_name=REGION)

    def invoke(self, session_id, messages):
        return self.client.invoke_harness(
            harnessArn=HARNESS_ARN,
            runtimeSessionId=session_id,
            messages=messages,
        )

    def read_stream(self, response):
        text = []
        tool = None
        stop_reason = None
        errors = []

        for event in response["stream"]:
            if "contentBlockStart" in event:
                start = event["contentBlockStart"].get("start", {})
                if "toolUse" in start:
                    t = start["toolUse"]
                    tool = {"toolUseId": t["toolUseId"], "name": t["name"],
                            "input": t.get("input"), "input_text": ""}

            if "contentBlockDelta" in event:
                delta = event["contentBlockDelta"].get("delta", {})
                if "text" in delta:
                    print(delta["text"], end="", flush=True)
                    text.append(delta["text"])
                if "toolUse" in delta and tool is not None:
                    piece = delta["toolUse"]
                    if "input" in piece:
                        if isinstance(piece["input"], str):
                            tool["input_text"] += piece["input"]
                        else:
                            tool["input"] = piece["input"]

            if "messageStop" in event:
                stop_reason = event["messageStop"].get("stopReason")

            if "runtimeClientError" in event:
                errors.append(event["runtimeClientError"].get("message", str(event["runtimeClientError"])))

        if tool and tool["input"] is None:
            raw = tool["input_text"].strip()
            tool["input"] = json.loads(raw) if raw else {}

        return {"text": "".join(text), "tool": tool, "stop_reason": stop_reason, "errors": errors}

    def run(self, prompt, session_id=None, max_tool_rounds=10):
        session_id = session_id or str(uuid.uuid4())
        print(f"Session: {session_id}")
        print(f"User: {prompt}\n")
        messages = [{"role": "user", "content": [{"text": prompt}]}]

        for i in range(max_tool_rounds + 1):
            print("Harness: ", end="", flush=True)
            parsed = self.read_stream(self.invoke(session_id, messages))
            print()

            if parsed["errors"]:
                raise RuntimeError("; ".join(parsed["errors"]))

            tool = parsed["tool"]
            if parsed["stop_reason"] != "tool_use" or tool is None:
                return parsed["text"]

            print("\n" + "=" * 70)
            print(f"INLINE FUNCTION REQUEST #{i + 1}")
            print(f"Function: {tool['name']}")
            print("Arguments:")
            print(json.dumps(tool["input"], indent=2))

            try:
                result = execute_tool(tool["name"], tool["input"])
                status = "success"
            except Exception as exc:
                result = {"error": str(exc)}
                status = "error"

            print("\nLOCAL PYTHON RESULT:")
            print(json.dumps(result, indent=2))
            print("=" * 70 + "\n")

            # AWS requires BOTH the assistant toolUse and matching user
            # toolResult in the follow-up invocation.
            messages = [
                {"role": "assistant", "content": [{"toolUse": {
                    "toolUseId": tool["toolUseId"],
                    "name": tool["name"],
                    "input": tool["input"],
                }}]},
                {"role": "user", "content": [{"toolResult": {
                    "toolUseId": tool["toolUseId"],
                    "content": [{"text": json.dumps(result)}],
                    "status": status,
                }}]},
            ]

        raise RuntimeError("Maximum client-side tool rounds exceeded")
