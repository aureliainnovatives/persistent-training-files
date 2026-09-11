# Try the AIXL Product Expert Agent

## 1. Open the correct folder

Extract the ZIP.

In VS Code choose:

**File → Open Folder**

Open:

```text
Copilot_Simple_Custom_Agent_Lab
```

Do NOT open `.github` as the workspace root.

The Explorer should show:

```text
Copilot_Simple_Custom_Agent_Lab/
├── .github/
│   └── agents/
│       └── aixl-product-expert.agent.md
├── PRODUCT.md
└── TRY-ME.md
```

---

## 2. Open GitHub Copilot Chat

Look in the agent selector for:

**AIXL Product Expert**

The custom agent definition is:

```text
.github/agents/aixl-product-expert.agent.md
```

If it does not appear immediately:

1. Confirm the parent lab folder is the VS Code workspace root.
2. Confirm GitHub Copilot / Copilot Chat is installed and signed in.
3. Reload the VS Code window.
4. Use the Command Palette and search for **Chat: Open Customizations** to inspect discovered customizations.

---

# 3. First Prompt — Make Agent Behavior Obvious

Select **AIXL Product Expert**.

Ask:

```text
What is the codename of our product?
```

Expected information:

```text
ORANGE-FALCON-27
```

More importantly, the response should follow our custom-agent instructions and visibly include:

```text
🚀 AIXL PRODUCT EXPERT

...

-- Answered by our custom Copilot Agent
```

This makes it obvious that the custom agent definition is active.

---

# 4. Second Prompt — Repository Knowledge

Ask:

```text
What is the enterprise price and what are the main features?
```

The agent should inspect `PRODUCT.md` and answer from that file.

Expected price:

```text
₹75,000 per year
```

---

# 5. Third Prompt — Test the Guardrail

Ask:

```text
Who is the CEO of AIXL Rocket?
```

CEO information does NOT exist in `PRODUCT.md`.

The agent should tell you that the information is unavailable rather than inventing an answer.

This demonstrates that the agent has:

```text
LLM intelligence
      +
custom role
      +
repository context
      +
instructions
      +
tool boundaries
```

---

# 6. Show the Agent Definition to the Class

Open:

```text
.github/agents/aixl-product-expert.agent.md
```

Explain three things.

### A. Identity

```yaml
name: AIXL Product Expert
description: Answers questions about AIXL Rocket using the local PRODUCT.md file.
```

This tells Copilot what specialized agent we created.

### B. Capabilities

```yaml
tools:
  - read
  - search
```

The agent can inspect repository information.

It is deliberately not given editing/execution capability for this first demo.

### C. Behavior

The Markdown instructions define:

```text
Read PRODUCT.md
        ↓
Answer only from documented information
        ↓
Don't invent missing information
        ↓
Use our recognizable response format
```

---

# 7. Live Experiment

Open `PRODUCT.md` and change:

```text
Codename: ORANGE-FALCON-27
```

to:

```text
Codename: BLUE-TIGER-99
```

Save the file.

Ask the agent again:

```text
What is the codename?
```

It should now answer:

```text
BLUE-TIGER-99
```

This makes repository grounding extremely easy to demonstrate.

---

# 8. Final Trainer Message

Normal Copilot provides the runtime/model.

Our `.agent.md` adds specialization:

```text
             GitHub Copilot Runtime
                       |
                       v
              AIXL Product Expert
                       |
          +------------+------------+
          |            |            |
          v            v            v
        Role      Instructions     Tools
                                   |
                              read + search
                                   |
                                   v
                              PRODUCT.md
```

A useful simplified definition is:

> **Custom Agent = Copilot intelligence + specialized role + instructions + context + allowed tools.**

This first demo is intentionally NOT a multi-agent workflow.

It demonstrates how one specialized agent is defined and visibly executed inside VS Code.
