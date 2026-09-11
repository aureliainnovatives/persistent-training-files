Level 3
LLM Evaluation
(LLM-as-a-Judge, Agent Evaluation, Human Evaluation)

# Level 3 — Modern LLM Evaluation

This is where enterprise AI has evolved.

## Human Evaluation

Experts manually score responses.

Typical dimensions:

-   Correctness
-   Helpfulness
-   Safety
-   Completeness
-   Tone
-   Groundedness

Still the gold standard, but expensive.

----------

## LLM-as-a-Judge

This is now widely used.

Example:

```
Prompt

Question

↓

Reference Answer

↓

Candidate Answer

↓

GPT-4 Judge

↓

Score

8.5 / 10
```

The judge evaluates:

-   correctness
-   completeness
-   reasoning
-   formatting

rather than exact wording.

This scales much better than human-only review.

----------

## Pairwise Evaluation

Instead of scoring independently:

```
Model A

vs

Model B

Which answer is better?
```

This reduces scoring bias.

Many modern leaderboards use this approach.

----------

## Arena-style Evaluation

Remember the website?

You were probably referring to **Chatbot Arena (LMSYS Arena)**.

Users compare two anonymous models and vote.

The ranking is built using Elo ratings, similar to chess.

It is one of the most influential public evaluations because it reflects human preferences.

----------

## Agent Evaluation

This is becoming the new frontier.

Evaluate:

-   Did the agent choose the correct tool?
-   Did it call APIs correctly?
-   Was the sequence of actions appropriate?
-   Did it recover from failures?
-   Was the final outcome successful?

Metrics include:

-   Task completion
-   Tool accuracy
-   Hallucinated tool calls
-   Planning quality
-   Number of retries
-   Cost
-   Latency

Frameworks such as **LangSmith**, **TruLens**, **DeepEval**, **Promptfoo**, **OpenAI Evals**, and **Ragas** support parts of this process.