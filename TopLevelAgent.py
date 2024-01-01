import chainlit as cl
from MergeDevAgents import *
from Utilities import *
from UserAgents import *
from langchain.memory import ConversationBufferWindowMemory, ConversationKGMemory, ChatMessageHistory

from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from typing import Optional

class TopLevelAgent:
    def __init__(self, config):
        self.config = config
        self.tools = [HumanInputTool(), HRISAgent(), PersonalInfoAgent(), CRMAgent()] # TODO: Also, add th KnowledgeGraphAgent here
        self.responsible_ai_agent = ResponsibleAIAgent()
        self.synthesis_agent = SynthesisAgent(config)
        self.history = ChatMessageHistory()
        self.kgLLM = OpenAI(temperature=0) # TODO: Move to config
        self.llm = ChatOpenAI(temperature=0.0)

        # We use ReACT + CoT prompting methodology for this advanced reasoning agent
        self.ai_agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # ReACT agent is best suited for this task.
            verbose=True, # TODO: Config
            memory=ConversationBufferWindowMemory(buffer_size=2)
            )
                                         
    def run(self, utterance: str, cb: Optional[cl.LangchainCallbackHandler] = None):
        if self.responsible_ai_agent.shouldFlag(utterance) or self.responsible_ai_agent.detectPromptInjection(utterance):
            return "Your ask violates Responsible AI guidelines. Please rephrase your ask."

        self.history.add_user_message(utterance)
        agent_response = self.ai_agent.run(utterance, callbacks=[cb] if cb else None)
        response_to_user = self.synthesis_agent.run(utterance, agent_response)
        self.history.add_ai_message(response_to_user)
        return response_to_user

