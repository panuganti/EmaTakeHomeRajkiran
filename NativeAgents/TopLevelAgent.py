### A general principle I follow while architecting LLM solution is as follows:
### 1. Use LLM only for complex reasoning tasks. For simple tasks, write the algorithm or use traditional ML models directly.
### 2. A single LLM must be given a task that you think an untrained-human can perform the task by reading at most 1 page of instructions.
### 3. If the task is complex, break it down into multiple tasks and use multiple LLMs.

### In many cases, Langchain abstractions take you away from the LLM, thus losing finer control over them. This is necessary for a scalable and debuggable design.
### However, Langchain has an amazing array of tools and abstractions. We leverage Langchain but try to keep our control over LLMs completely.

from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

# Define the agent
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage

## Import all the tools
from MergeDevAgents import *
from Utilities import *
from UserAgents import *

class TopLevelAgent:
    def __init__(self, config):
        self.config = config
        self.tools = [HRISAgent(), PersonalInfoAgent(), CRMAgent()]
        self.responsible_ai_agent = ResponsibleAIAgent()

        # We use ReACT + CoT prompting methodology for this advanced reasoning agent
        self.ai_agent = initialize_agent(self.tools,
                            # TODO: We need an advanced LLM here that follows the instructions diligently.
                            ChatOpenAI(model="gpt-4-0613", temperature=0, max_tokens=1000),
                            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                            verbose=True)

    def run(self, utterance: str):
        # Perform Responsible AI Checks
        if (self.responsible_ai_agent.shouldFlag(utterance)):
            return "Your ask violates Responsible AI guidelines. Please rephrase your ask."

        if (self.responsible_ai_agent.detectPromptInjection(utterance)):
            return "Your ask violates Responsible AI guidelines. Please rephrase your ask."

        return self.ai_agent.run(utterance)
