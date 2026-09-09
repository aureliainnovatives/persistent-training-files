from harness_client import HarnessClient

PROMPT = (
    "Investigate incident INC-2026-0908-017. Determine the affected service, "
    "inspect its operational metrics, and explain what is most likely happening. "
    "Use the available tools rather than guessing."
)


if __name__ == "__main__":
    HarnessClient().run(PROMPT)