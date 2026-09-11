# Module 3.4 --- HITL, Protocols & Security

This pack contains trainer notes, architecture diagrams, and a runnable
LangChain Human-in-the-Loop demonstration.

## Files

``` text
Module_3_4_HITL_Protocols_Security/
├── 01-Trainer-Guide.md
├── 02-HITL-LangChain-Demo/
│   ├── hitl_operations_agent.py
│   ├── TRY-ME.md
│   ├── requirements.txt
│   └── .env.example
└── 03-Architecture-Diagrams.md
```

## Recommended order

1.  Teach the HITL authority-boundary concept from
    `01-Trainer-Guide.md`.
2.  Show the risk gate and pause/resume diagrams.
3.  Run the safe read-only prompt.
4.  Run a restart prompt and approve it.
5.  Run again and reject the protected action.
6.  Discuss why middleware enforcement is stronger than prompt-only
    guidance.
7.  Close with protocol identity, delegation, least privilege, and
    auditability.

## Technical note

The hands-on uses LangChain's current agent-level Human-in-the-Loop
middleware. LangChain HITL uses LangGraph persistence underneath for
pause/resume state, but students interact primarily with the LangChain
`create_agent` and middleware APIs.
