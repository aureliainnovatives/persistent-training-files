# FDE-MM Group Activity 05 --- Software Modernization Assistant

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

An enterprise wants AI to accelerate modernization of a large
**Java/Spring application portfolio**.

-   Thousands of source files exist across multiple repositories.
-   Teams want code explanation, migration recommendations, code
    changes, and unit tests.
-   Internal coding standards and architecture guidelines are
    documented.
-   Generated code must compile and pass regression tests.
-   Some applications are business-critical.
-   The customer wants to select one enterprise model for the entire
    program.

The customer says:

> **"Let's choose whichever coding model scores highest on public
> benchmarks and use it across every repository."**

## Your Mission

**You are the FDE team. Decide how model selection should actually
work.**

  --------------------------------------------------------------------------------------
  \#             Decision Question     Options             Your Choice    Why? --- 1
                                                                          line only
  -------------- --------------------- ------------------- -------------- --------------
  1              What should the model Explain / Recommend                
                 be allowed to do?     / Generate code /                  
                                       Directly merge code                

  2              Where should internal Model / Prompt /                   
                 standards come from?  RAG / Fine-tuning                  

  3              How should            Entire repo in                     
                 repository-specific   prompt /                           
                 context reach the     Retrieval/context                  
                 model?                selection /                        
                                       Fine-tuning                        

  4              What is the strongest Human-like code /                  
                 success metric?       Benchmark score /                  
                                       Compile + test                     
                                       success / Response                 
                                       length                             

  5              How should models be  Public leaderboard                 
                 selected?             / Vendor /                         
                                       Customer-specific                  
                                       eval / Largest                     
                                       context window                     

  6              What happens when     Accept / Retry                     
                 generated code fails  blindly / Diagnose                 
                 tests?                failure / Human                    
                                       review                             

  7              Should the same model Yes / No / Evaluate                
                 handle every coding   by task / Largest                  
                 task?                 model always                       

  8              Would you fine-tune   Yes / No / Maybe                   
                 on the codebase       after baseline eval                
                 immediately?                                             
  --------------------------------------------------------------------------------------

## Final Recommendation

> **We recommend
> \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
> because
> \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.**
