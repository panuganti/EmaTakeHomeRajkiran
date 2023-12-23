## EMA-TakeHome-Rajkiran (TODO: Replace with a ProjectSpecificName)
Search across work apps with AI enterprise search.

## Plan of Execution
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


## Overview

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


## Scenario 5: What fraction of P0 bugs in my organization has been fixed within SLA?
1. Where to look for SLA ? If found, great, else, ask user
2. Get list of bugs fixed
3. Compute the create and completed date filter

## Scenario 6: For my team in bangalore, tell me the count of tickets assigned to each of them, and how many rounds of interview they each had.
1. Get list of employees in my team in Bangalore
2. For each, get the count of tickets assigned
3. For each, how many rounds of interview they had.

### TODO: Explore Autogen and Create agents for each of them


## Description
An enterprise has several enterprise applications. On average an enterprise uses 150+ applications, each with 20+ APIs on average. There are 7000+ enterprise applications in the market.
We plan to leverage/constrain ourselves with the integrations provided by merge.dev for this MVP.

### About Merge.Dev

Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.




## Installation
## Usage
## Roadmap
## Contributing
## Authors and acknowledgment
## License
## TODOs


