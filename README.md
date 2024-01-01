## EMA-TakeHome-Rajkiran (TODO: Replace with a ProjectSpecificName)
Search across work apps with AI enterprise search.

## How to run
The UI is built with Chainlit. To run the application, please follow the following steps:
Step 1. pip install -r requirements.txt
Step 2. chainlit run app.py  -- You will see a browser window open with Chat Interface
Step 3. Try the following message: What's my time off balance ?
Step 4. Try the second scenario: Summarize my last conversation with Bill’s company

The mock-up data has been enabled for these scenarios. You can try various variations that uses this data.
For enabling this app to other scenarios, we either need a merge.dev keys integrated with real applications Or, I need to mock more data.

## Design Overview




## Execution plan for this project.
1. Understand the merge.dev categories and the models
2. Create few compelling scenarios:
    a. Querying only one source
    b. Querying multiple sources and joining information across -- More like ReAct

     Work through each of these scenarios: 
    Summarize my last conversation with Bill’s company
How many vacations do I have remaining?
What is the total HC cost for each of my managers?
How much revenue does the top 10 customers bring in?
What fraction of P0 bugs in my organization has been fixed within SLA?
How many leads have we not met yet?
Tell me the pending time off requests for my team members in Bangalore.
For my team in bangalore, tell me the count of tickets assigned to each of them, and how many rounds of interview they each had.

    c. Clarifying questions scenario
    d. Address staleness of data stored/cached -- Memory/preference storage -- (ex: modeling of user)
    e. Knowledge graph scenarios


## Design

Categories: HRIS, ATS, Accounting, Ticketing, CRM, Marketing Automation, File Storage
Models:
HRIS: (HR, Payroll and Directory)
BankInfo, Benefit, Company, Dependent, Employee, EmployeePayrollRun, EmployerBenefit, Employment, Group, Location, PayGroup, PayrollRun, Team, TimeOff, TimeOffBalance, TimesheetEntry

ATS: (Recruiting)
Accounting:
Ticketing
CRM:
Marketing Automation
File Storage:

## Scenario 1: Summarize my last conversation with Bill's company
1. Intent: Get Last Conversation
2. Entity: Bill's company ... Get list of all contacts, search for bill's
  -- Get Bill from complete list of contacts, if there are more than 1 bill, resolve which bill
3. if there are many disambiguate with user.
4. Get last conversation with company

## Scenario 2: How many vacations do I have remaining?
1. Resolve 'me'
2. Determine that Time-Off-Balances is the function that will answer
3. Get the answer

## Scenario 3: What is the total HC cost for each of my managers?
-- Better to write code. Isn't it ?
1. Get 'me'
2. Get list of 'me' manager ids... recursively look up their managers...
3. Get list of all employees and their employees recursively. 
4. For each employee, get the cost
5. Aggregate (Sum) of cost for all employees

## Scenario 4: How much revenue does the top 10 customers bring in?
1. 

## Scenario 5: What fraction of P0 bugs in my organization has been fixed within SLA?
1. Where to look for SLA ? If found, great, else, ask user
2. Get list of bugs fixed
3. Compute the create and completed date filter

## Scenario 6: For my team in bangalore, tell me the count of tickets assigned to each of them, and how many rounds of interview they each had.
1. Get list of employees in my team in Bangalore
2. For each, get the count of tickets assigned
3. For each, how many rounds of interview they had.


## Important TODOs:
1. 

## Architecture and Instructions for L5 Developers to complete/extend this project  

