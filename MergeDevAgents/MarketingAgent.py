from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage

from langchain.tools import BaseTool
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

class MarketingAgent(BaseTool):
    name = "MarketingAgent"
    description = "The MarketingAgent is used to represent current balances in hours for an employee's Time Off plan. I take input in a natural language format.\
                    The information broadly falls into the following categories. \
                    1. The Action object is used to represent an action (sending emails, messages etc.) executed within an automation.\
                    2. The Automation object is used to represent an automation, workflow or custom event in the system.\
                    3. The Campaign object is used to represent a marketing campaign.\
                    4. The Contact object is used to represent a contact in the system.\
                    5. The MarketingEmail object is used to represent a marketing email in the system.\
                    6. The Event object is used to represent a marketing event, such as a webinar or email, in the system.\
                    7. The List object is used to represent a list of contacts in the system.\
                    8. The MarketingMessage object is used to represent a marketing message in the system.\
                    9. The Template object is used to represent a template for a marketing asset in the system.\
                    10. The User object is used to represent a user in the system.\
                    "

    def _run(self, utterance: str):
        tools = []
        ai_agent = initialize_agent(tools,
                            # The task here is straightforward. Hence, gpt-3.5-turbo is sufficient.
                            # For cost optimization, we can replace this agent with a combination of Intent-Detection & Entity/Slot Extraction
                            ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, cache=False),
                            agent=AgentType.OPENAI_FUNCTIONS,
                            handle_parsing_errors=True,
                            verbose=False)
        response = ai_agent.run(utterance)
        return response

    def _arun(self, utterance: str):
        raise NotImplementedError("This tool does not support async")


from merge.client import Merge

