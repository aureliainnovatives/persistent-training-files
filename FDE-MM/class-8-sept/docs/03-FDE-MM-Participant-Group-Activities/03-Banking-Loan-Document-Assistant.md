# FDE-MM Group Activity 03 --- Banking Loan Document Assistant

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

A bank wants AI to review loan applications and supporting documents
before they reach a credit officer.

-   Applications contain salary slips, bank statements, forms, and
    free-text notes.
-   Eligibility rules are explicitly defined by the bank.
-   Customer/account information is available through internal APIs.
-   Incorrect decisions can have regulatory and customer impact.
-   The bank wants to reduce manual review time.
-   The AI must explain what evidence led to its recommendation.

The customer says:

> **"A powerful reasoning model should be able to read everything and
> approve or reject the loan."**

## Your Mission

**You are the FDE team. Decide where the model's responsibility should
end.**

  ---------------------------------------------------------------------------
  \#             Decision       Options         Your Choice    Why? --- 1
                 Question                                      line only
  -------------- -------------- --------------- -------------- --------------
  1              Best role for  Extract /                      
                 the model?     Summarize /                    
                                Recommend /                    
                                Final approval                 

  2              Where should   Prompt / Model                 
                 eligibility    reasoning /                    
                 rules execute? Deterministic                  
                                code /                         
                                Fine-tuning                    

  3              Where should   Model /                        
                 current        Documents / API                
                 customer data  Tool                           
                 come from?                                    

  4              How should     Free text /                    
                 model output   Structured                     
                 be returned?   output /                       
                                Explanation                    
                                only / JSON +                  
                                evidence                       

  5              What should    Guess / Retry /                
                 happen on      Human review /                 
                 ambiguous      Reject                         
                 documents?     application                    

  6              How would you  Benchmark /                    
                 compare        Extraction +                   
                 models?        reasoning eval                 
                                / Model size /                 
                                Vendor                         
                                reputation                     

  7              Which failure  Slow wording /                 
                 matters most?  Wrong evidence                 
                                / Long response                
                                / Different                    
                                writing style                  

  8              Should the LLM Yes / No / Only                
                 make the final defined cases                  
                 credit                                        
                 decision?                                     
  ---------------------------------------------------------------------------

## Final Recommendation

> **We recommend
> \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
> because
> \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.**
