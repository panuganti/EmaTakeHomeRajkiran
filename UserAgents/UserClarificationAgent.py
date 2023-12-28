
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage # delete ?

from langchain.tools import BaseTool

class UserClarificationAgent(BaseTool):
    name = "UserClarificationAgent"
    description = "The UserClarificationAgent is used whenever a clarification is required from the user for making a choice. \
        For example, if we need to determine which of the two Steve's is relevant, this agent takes as input information about all the Steve's and presents to the user for selection."

    def _run(self, thought: str):
        # Ask the user which one is relevant and get the answer
        # Read user input and store it in a variable
        user_response = input(f"Please help us with this selection: {thought}")
        return user_response

    def _arun(self, thought: str):
        raise NotImplementedError("This tool does not support async")

