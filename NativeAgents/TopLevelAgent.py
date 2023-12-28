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
from langchain.memory import ConversationBufferWindowMemory, ConversationKGMemory, ChatMessageHistory

# TODO: 
# 1. Enable Streaming support - for masking latency
# 2. Incorporate Fallbacks - for robustness
# 3. Integrate with Langsmith - For logging and debugging
# 4. 


class TopLevelAgent:
    def __init__(self, config):
        self.config = config
        self.merge_dev_tools = [HRISAgent(), PersonalInfoAgent(), CRMAgent()]
        self.responsible_ai_agent = ResponsibleAIAgent()
        self.synthesis_agent = SynthesisAgent(config)
        self.history = ChatMessageHistory()

        # We use ReACT + CoT prompting methodology for this advanced reasoning agent
        self.ai_agent = initialize_agent(self.merge_dev_tools,
                            # TODO: We need an advanced LLM here that follows the instructions diligently. So, we use GPT-4 here.
                            ChatOpenAI(model="gpt-4-0613", temperature=0, max_tokens=1000),
                            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                            verbose=True,
                            memory=ConversationBufferWindowMemory(buffer_size=2) # TODO: make it configurable. Also, keep the window small.
                            )

    def set_new_session(self):
        self.history = ChatMessageHistory()
        self.ai_agent.set_new_session()

    def run(self, utterance: str):
        # Perform Responsible AI Checks
        if (self.responsible_ai_agent.shouldFlag(utterance)):
            return "Your ask violates Responsible AI guidelines. Please rephrase your ask."

        if (self.responsible_ai_agent.detectPromptInjection(utterance)):
            return "Your ask violates Responsible AI guidelines. Please rephrase your ask."

        self.history.add_user_message(utterance)
        agent_response = self.ai_agent.run(utterance)

        # We are using custom Synthesis agent instead of a Output Parser in order to keep the output more natural.
        response_to_user = self.synthesis_agent.run(utterance, agent_response)
        # self.history.add_ai_message(response_to_user)
        return response_to_user

