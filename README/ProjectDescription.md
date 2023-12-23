# Scenario:
An enterprise has several enterprise applications. On average an enterprise uses 150+ applications, each with 20+ APIs on average. There are 7000+ enterprise applications in the market. 
Example categories are:
HR: Workday
Sales: CRM (Salesforce)
Ticketing: JIRA
Check https://merge.dev/ for application categories.

Hint: [Configurable set of apis at tenant level]

# Problem Statement 
Design and Build a multi-tenant Conversational AI system over the structured data stored in these applications.

# Example Use cases:
1. Summarize my last conversation with Bill’s company
2. How many vacations do I have remaining?
3. What is the total HC cost for each of my managers?
4. How much revenue does the top 10 customers bring in?
5. What fraction of P0 bugs in my organization has been fixed within SLA?
6. How many leads have we not met yet?
7. Tell me the pending time off requests for my team members in Bangalore.
8. For my team in bangalore, tell me the count of tickets assigned to each of them, and how many rounds of interview they each had.

# Enterprise constraints:
1. We are a startup, training data initially is hard. 
Hint: if fine-tuning/regression etc. is required in any scenarios) 
2. We need to worry about cost and user interactiveness
[Raj]: User-Interactiveness is P0. (Quicker response, and clarifying questions, Cost, though secondary, but think how to minimize)
3. The answer to the user's questions needs to be accurate or the conversation should gracefully degrade.
4. Staleness: Think about staleness … of the data that we might store in our intermediate system from the primary api source.
[Raj]: Direct to API.. don’t worry about staleness.. We can also store data somewhere.. Ex: code etc.. 
5. need to think about common models for linking different domains
[Raj]: might not be straight forward to join data from across models (hint: knowledge graphs)
Several user’s questions is not a simple API lookup. It may require access to multiple APIs.


# Expected Outcome
1. Detailed and comprehensive design. 
Assume that it will be a 6+ month long project to fully complete
[Many places there are options & recommendations] -- don’t worry about how much time to implement.. Target audience is L5 engineers..

2. Pick a scenario, implement using any library of your choice. Add it in your Github/Gitlab. Share with souvik-sen@. The scenario you pick is your choice and demonstrates your technical leadership. Ideas could be to de-risk an unknown in the implementation or build out an overall framework first.

# Evaluation: [Raj]
1. Design should meet the requirements
2. Comprehensive… At least have a recommended answer
3. Think like L7 and your Target engineers who will implement are your juniors (L5).
4. Implementation (P1 -- doesn’t matter much): ‘What scenario you are picking’ part is important. -- Demo is less important than picking a good scenario (P0).
