# FDE-MM Group Activity 04 --- Manufacturing Maintenance Copilot

**Time:** 30 minutes\
**Team:** 4--5 participants\
**Deliverable:** Complete the grid and agree on one final
recommendation.

## Agenda

  Time     Activity
  -------- -------------------------------
  3 min    Read the customer situation
  15 min   Complete the decision grid
  5 min    Agree on final recommendation
  7 min    Share and compare decisions

## Customer Situation

A manufacturing company wants an AI copilot for technicians
troubleshooting production equipment.

-   Equipment manuals and repair procedures are available as documents.
-   Historical maintenance tickets are available.
-   Current sensor readings and machine state come from live systems.
-   Some repair actions can stop the production line.
-   Safety procedures must always be followed.
-   Technicians want quick troubleshooting recommendations.

The customer says:

> **"Let's train the model on all our manuals and historical tickets so
> it knows our machines."**

## Your Mission

**You are the FDE team. Decide what the model should know, retrieve, and
obtain live.**

  -----------------------------------------------------------------------------------
  \#             Decision Question     Options          Your Choice    Why? --- 1
                                                                       line only
  -------------- --------------------- ---------------- -------------- --------------
  1              What should the model Diagnose /                      
                 primarily do?         Recommend /                     
                                       Execute repair /                
                                       Explain evidence                

  2              Where should          Model / RAG /                   
                 manuals/procedures    Fine-tuning /                   
                 come from?            Prompt                          

  3              Where should live     RAG / Model /                   
                 sensor state come     API Tool /                      
                 from?                 Fine-tuning                     

  4              How should safety     Prompt only /                   
                 rules be enforced?    Model judgment /                
                                       Deterministic                   
                                       controls /                      
                                       Ignore                          

  5              What should           RAG / Evaluation                
                 historical tickets be / Fine-tuning /                 
                 used for?             Combination                     

  6              What happens before a Automatic /                     
                 production-stopping   Model                           
                 action?               confirmation /                  
                                       Human approval /                
                                       Retry                           

  7              How would you         Fluency /                       
                 evaluate model        Correct                         
                 quality?              diagnosis + safe                
                                       recommendation /                
                                       Benchmark /                     
                                       Speed only                      

  8              Would fine-tuning be  Yes / No / Only                 
                 your first step?      after evaluation                
  -----------------------------------------------------------------------------------

## Final Recommendation

> **We recommend
> \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
> because
> \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.**
