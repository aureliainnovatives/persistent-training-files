# TRY-ME --- LangChain Human-in-the-Loop Lab

## Objective

Demonstrate that an LLM may **propose** a consequential tool call
without automatically receiving authority to execute it.

The demo uses LangChain's `HumanInTheLoopMiddleware`.

------------------------------------------------------------------------

## 1. Setup

Create and activate a virtual environment if desired, then:

``` bash
python -m pip install -r requirements.txt
```

Copy:

``` text
.env.example
```

to:

``` text
.env
```

Add your API key.

The default configuration uses the standard OpenAI endpoint.
`OPENAI_BASE_URL` and `OPENAI_MODEL` are kept configurable for
classroom/provider flexibility.

------------------------------------------------------------------------

## 2. Run

``` bash
python hitl_operations_agent.py
```

------------------------------------------------------------------------

## 3. Recommended Demo Prompts

### Prompt A --- Safe read operation

``` text
Check the health of payment-service and tell me what you find. Do not restart or rollback anything.
```

Expected teaching point:

``` text
read_service_health
        ↓
executes automatically
```

No human approval should be required because the read tool is configured
as safe.

------------------------------------------------------------------------

### Prompt B --- Restart requiring approval

``` text
The payment-service is unhealthy. Check its health and restart it if that is the appropriate recovery action.
```

If the model proposes `restart_service`, the HITL middleware pauses
before tool execution.

The terminal shows the pending action and asks:

``` text
Approve this action? [y/n]
```

Choose `y` to demonstrate:

``` text
Agent proposes action
        ↓
HITL middleware interrupts
        ↓
Human approves
        ↓
Tool executes
        ↓
Agent resumes
```

------------------------------------------------------------------------

### Prompt C --- Reject the action

``` text
Check inventory-service and restart it if needed.
```

When approval is requested, choose `n`.

The rejection is returned to the agent as feedback. Observe how the
agent responds without the protected tool being executed.

------------------------------------------------------------------------

### Prompt D --- Rollback

``` text
payment-service started failing immediately after deployment v2.7. Check the service and rollback to v2.6 if appropriate.
```

`rollback_deployment` is also protected by the approval policy.

------------------------------------------------------------------------

## 4. Show the Code to the Class

Focus on this policy:

``` python
HumanInTheLoopMiddleware(
    interrupt_on={
        "restart_service": {
            "allowed_decisions": ["approve", "reject"],
            "description": "Production service restart requires operator approval.",
        },
        "rollback_deployment": {
            "allowed_decisions": ["approve", "reject"],
            "description": "Production rollback requires operator approval.",
        },
        "read_service_health": False,
    }
)
```

This is the core architectural idea:

``` text
SAFE TOOL
read_service_health
        ↓
automatic

SIDE-EFFECT TOOL
restart / rollback
        ↓
HITL approval boundary
```

------------------------------------------------------------------------

## 5. Important Discussion

Ask participants:

> Why not simply put "ask before restarting production" in the system
> prompt?

Expected answer:

A prompt is behavioral guidance. Middleware/tool policy is an
**execution control**. For consequential operations, enforcement should
exist at the action boundary rather than relying only on the model
remembering an instruction.

------------------------------------------------------------------------

## 6. Extend the Lab

After the basic demo, ask participants to add another tool:

``` text
delete_customer_data
```

Then decide:

1.  Should it support approve/reject?
2.  Should it be completely unavailable?
3.  Which identity should be allowed to approve it?
4.  What evidence should the approval screen display?
5.  What audit information should be stored?

This moves the discussion from coding into enterprise architecture.
