from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage

from langchain.tools import BaseTool
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

class TicketingAgent(BaseTool):
    name = "TicketingAgent"
    description = "The TicketingAgent is used to get information related to Ticketing. It takes input in a natural language format.\
                    The information broadly falls into the following categories. \
                    1. The Ticket object is used to represent a ticket or a task within a system.\
                    2. The User object is used to represent an employee within a company.\
                    3. The account is a company that may be a customer. This does not represent the company that is receiving the ticket.\
                    4. The Attachment object is used to represent an attachment for a ticket.\
                    5. The Comment object is used to represent a comment on a ticket.\
                    6. The Collection object is used to represent collections of tickets. Collections may include other collections as sub collections.\
                    7. The Contact object is used to represent the customer, lead, or external user that a ticket is associated with.\
                    8. The Role object is used to represent the set of actions & access that a user with this role is allowed to perform.\
                    9. The Tag object is used to represent a tag or label for a ticket.\
                    10. The Team object is used to represent a team within the company receiving the ticket.\
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

