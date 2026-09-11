# Multi-Agent Topologies & Patterns

  -----------------------------------------------------------------------------------
  Pattern                Shape             Best use          Watch-out
  ---------------------- ----------------- ----------------- ------------------------
  Supervisor/Subagents   Supervisor →      Central           Supervisor bottleneck
                         specialists →     accountability    
                         supervisor                          

  Router                 Classify →        Distinct domains  Routing accuracy
                         specialist(s) →                     
                         synthesize                          

  Sequential             A → B → C         Ordered stages    Error propagation

  Handoff                A transfers       Stage/role        State/context transfer
                         control to B      transition        

  Hierarchical           Manager → teams   Complex           Coordination cost
                                           decomposition     

  Peer-to-peer           A ↔ B ↔ C         Direct            Ownership/loops
                                           collaboration     

  Group Chat             Shared thread     Iterative         Context/token growth
                                           perspectives      

  Swarm                  Dynamic handoffs  Open-ended work   Governance/termination

  Graph/State Machine    Nodes +           Production        More explicit design
                         conditional edges control           
  -----------------------------------------------------------------------------------

## Trainer rule

-   Known path → workflow/graph.
-   Known domains, uncertain destination → router.
-   One accountable coordinator → supervisor.
-   Conversational stage change → handoff.
-   Collaborative discussion → group chat.
-   Highly dynamic delegation → swarm, only when justified.
