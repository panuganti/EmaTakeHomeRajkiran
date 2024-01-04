"""Tool for asking human input."""

from typing import Callable, Optional

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseTool
import chainlit as cl
import asyncio

def _print_func(text: str) -> None:
    print("\n")
    print(text)


class HumanInputTool(BaseTool):
    """Tool that asks user for input."""

    name: str = "Human"
    description: str = (
        "You can ask a human for disambiguation when you have to make a choice and you do not have enough information to make the choice."
        "The input should be a detailed question with entire observation for the human to answer."
    )
    prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        # self.prompt_func(query)
        res = asyncio.run(cl.AskUserMessage(content=query).send())
        if res:
            return res['content']
        
    async def _arun(self, query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
        """Use the Human input tool."""
        # self.prompt_func(query)
        res = await cl.AskUserMessage(content=query).send()
        if res:
            return res['content']    