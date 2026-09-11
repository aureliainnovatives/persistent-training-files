# FDE-MM Group Activity 01 --- Insurance Claims Assistant

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

An insurance company processes **40,000 motor claims per month** and
wants AI to identify claims that may require investigation.

-   Claims policies change every few months.
-   Current claim information is available through an API.
-   Three years of reviewed historical claims are available.
-   Missing a suspicious claim is expensive.
-   Incorrectly flagging a genuine customer is also undesirable.
-   Target response time is under 5 seconds.

The customer says:

> **"We have lots of historical data. Let's fine-tune the best LLM and
> let it classify every claim."**

## Your Mission

**You are the FDE team. Do you agree?**

  -------------------------------------------------------------------------------
  \#             Decision       Options             Your Choice    Why? --- 1
                 Question                                          line only
  -------------- -------------- ------------------- -------------- --------------
  1              What should    Extract / Recommend                
                 the model do?  / Decide / Decide +                
                                Act                                

  2              Where should   Model / Prompt /                   
                 changing       RAG / Fine-tuning                  
                 policy                                            
                 knowledge come                                    
                 from?                                             

  3              Where should   Model / RAG / API                  
                 current claim  Tool                               
                 data come                                         
                 from?                                             

  4              What should we RAG / Fine-tune /                  
                 do with 3      Evaluation dataset                 
                 years of       / Combination                      
                 historical                                        
                 claims?                                           

  5              How would you  Biggest / Cheapest                 
                 choose the     / Evaluate 2--3                    
                 model?         models / Fine-tuned                

  6              What happens   Accept / Retry /                   
                 when the model Stronger model /                   
                 is uncertain?  Human review                       

  7              What would     Overall accuracy /                 
                 prove          Demo /                             
                 production     Customer-specific                  
                 readiness?     evaluation / Public                
                                benchmark                          

  8              Would you      Yes / No / Maybe                   
                 fine-tune now? later                              
  -------------------------------------------------------------------------------

## Final Recommendation

> **We recommend
> \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
> because
> \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.**
