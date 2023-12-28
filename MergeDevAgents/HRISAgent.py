from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage

from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

class HRISAgent(BaseTool):
    name = "HRISAgent"
    description = "The HRISAgent object is used to represent current balances in hours for an employee's Time Off plan. I take input in a natural language format."

    def _run(self, utterance: str):
        tools = [TimeOffBalanceTool()]
        ai_agent = initialize_agent(tools,
                            # The task here is straightforward. Hence, gpt-3.5-turbo is sufficient.
                            # For cost optimization, we can replace this agent with a combination of Intent-Detection & Entity/Slot Extraction
                            ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, cache=False),
                            agent=AgentType.OPENAI_FUNCTIONS,
                            verbose=False)
        response = ai_agent.run(utterance)
        return response

    def _arun(self, utterance: str):
        raise NotImplementedError("This tool does not support async")


from merge.client import Merge
from merge.resources.hris import TimeOffBalancesListRequestPolicyType

class HRIS:
    # TODO: List all the methods that are available in the HRIS API
    def get_time_off_balances(self, employee_id: str):
        return 10;

class TimeOffCheckInput(BaseModel):
    """Input for checking time off balance."""

    employee_id: str = Field(..., description="Employee Id")

class TimeOffBalanceTool(BaseTool):
    name = "get_time_off_balances"
    description = "The TimeOffBalance object is used to represent current balances in hours for an employee's Time Off plan."

    def _run(self, employee_id: str):
        hris = HRIS()
        return hris.get_time_off_balances(employee_id)

    def _arun(self, employee_id: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = TimeOffCheckInput


