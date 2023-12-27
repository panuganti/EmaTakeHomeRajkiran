
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage # delete ?

from langchain.tools import BaseTool

class UserClarificationAgent(BaseTool):
    name = "UserClarificationAgent"
    description = "The UserClarificationAgent is used whenever a clarification is required for making a choice. \
        For example, if we need to determine which of the two Steve's is relevant, this agent will be used to clarify."

    def _run(self, utterance: str):
        # Ask the user which one is relevant and get the answer
        # Read user input and store it in a variable
        user_response = input(f"Please help us with this clarification: {utterance}")
        return user_response

    def _arun(self, utterance: str):
        raise NotImplementedError("This tool does not support async")

