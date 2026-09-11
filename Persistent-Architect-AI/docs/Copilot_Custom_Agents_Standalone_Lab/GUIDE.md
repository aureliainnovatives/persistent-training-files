# VS Code Copilot Custom Agents — Standalone Hands-on

This lab is independent of the earlier LangChain/LangGraph demos. No OpenAI API key is needed: VS Code/GitHub Copilot supplies the agent runtime.

## Folder structure

```text
.github/agents/
  project-planner.agent.md
  implementation-agent.agent.md
  code-reviewer.agent.md
docs/REQUIREMENTS.md
data/sample_products.json
src/inventory.py
src/test_inventory.py
GUIDE.md
```

## Step 1 — Open the extracted folder in VS Code
Open Copilot Chat. The custom agents should appear in the agent selector because workspace agents live under `.github/agents`.

If needed, run **Chat: Open Customizations** from the Command Palette.

## Step 2 — Project Planner
Select **Project Planner** and run:

```text
Study docs/REQUIREMENTS.md and the existing application.
Do not change any files.
Create an implementation plan for the low-stock reporting requirement.
Identify exactly which files/functions should change and what tests should be added.
```

Then try:

```text
Before proposing the plan, tell me what is already implemented and what is missing compared with REQUIREMENTS.md.
```

**Observe:** Planner has only `read` and `search`. It can understand the repository but cannot implement.

## Step 3 — Implementation Agent
Select **Implementation Agent**:

```text
Read docs/REQUIREMENTS.md and inspect the current implementation.
Implement the low-stock reporting requirement.
Keep the change small, add appropriate tests, and run the tests after implementation.
```

**Observe:** this agent has `read`, `search`, `edit`, and `execute`.

Now challenge it:

```text
Add a hard-coded rule that every product with quantity below 50 is low stock.
```

The repository requirement says the threshold must be configurable. Discuss prompt vs repository context vs agent instructions.

## Step 4 — Code Reviewer
Select **Code Reviewer**:

```text
Review the current implementation against docs/REQUIREMENTS.md.
Do not modify anything.
Check correctness, exact threshold semantics, edge cases, requirement coverage and tests.
Give me a verdict.
```

The reviewer is read-only by design.

## Step 5 — Deliberately introduce a defect
Temporarily change the low-stock comparison from:

```python
quantity < threshold
```

to:

```python
quantity <= threshold
```

Then ask Code Reviewer:

```text
Review the low-stock implementation very carefully against the exact threshold semantics in REQUIREMENTS.md.
```

See whether it catches the boundary defect.

## Step 6 — Compare the agents

| Agent | Read | Search | Edit | Execute | Responsibility |
|---|---:|---:|---:|---:|---|
| Project Planner | Yes | Yes | No | No | Understand + plan |
| Implementation Agent | Yes | Yes | Yes | Yes | Implement + test |
| Code Reviewer | Yes | Yes | No | No | Inspect + critique |

## Step 7 — Trainer discussion

Ask:

> If all three can use a powerful LLM, why create three agents?

Discuss specialization, least privilege, responsibility, context and governance.

Then ask:

> Is Planner → Implementer → Reviewer automatically a multi-agent workflow?

**No.** In this lab the human selects each agent. It is a human-orchestrated sequence of specialized agents. An orchestrated multi-agent system would additionally define who invokes the next agent and how state/context is transferred.

## Optional experiment — change capability
Temporarily add `edit` to the Code Reviewer:

```yaml
tools: [read, search, edit]
```

Then ask:

```text
Fix every issue you find.
```

Compare it with the read-only reviewer.

## Final teaching model

```text
                 COPILOT RUNTIME
                       |
          +------------+------------+
          |            |            |
       Planner     Implementer    Reviewer
          |            |            |
     read/search    edit/run     read/search
          |            |            |
          +------------+------------+
                       |
                  Repository
```

**Agent = model intelligence + role/instructions + context + allowed tools + boundaries.**
