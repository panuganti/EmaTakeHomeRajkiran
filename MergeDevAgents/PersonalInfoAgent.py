from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage

from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

class PersonalInfoAgent(BaseTool):
    name = "PersonalInfoAgent"
    description = "This  tool helps retrieve information about the myself like my employee id, my name etc. I take input in a natural language format."

    def _run(self, utterance: str):
        tools = [PersonalInfoTool()]
        ai_agent = initialize_agent(tools,
                            ChatOpenAI(model="gpt-3.5-turbo-0613"),
                            agent=AgentType.OPENAI_FUNCTIONS,
                            verbose=True)
        response = ai_agent.run(utterance)
        return response

    def _arun(self, utterance: str):
        raise NotImplementedError("This tool does not support async")


from merge.client import Merge
from merge.resources.hris import TimeOffBalancesListRequestPolicyType
from pydantic import BaseModel, Field

class PersonalInfo:
    # This class is used to retrieve personal information about the user.
    # This is only a mock. This class is to be replaced retrieval using Merge.Dev API
    # In other words, the data retrieved here will not be stale.

    dict = {"employee_id": "12345", "email": "john.doe@gmail.com"}

    def get_value(self, key: str):
        if key not in self.dict:
            return "Information about " + key + " is not available"
        return self.dict[key];

class PersonalInfoCheckInput(BaseModel):
    """Input for retrieving personal information."""

    property: str = Field(..., description="Personal Information property to retrieve. The keys are always in lower case. Valid values are employee_id, name and email")

class PersonalInfoTool(BaseTool):
    name = "personal_info_tool"
    description = "The PersonalInfo tool is used to represent current balances in hours for an employee's Time Off plan."

    def _run(self, property: str):
        personal_info = PersonalInfo()
        value = personal_info.get_value(property)
        return value

    def _arun(self, property: str):
        # TODO: Implement async version of this method
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = PersonalInfoCheckInput


