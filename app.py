from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

from langchain.chains import LLMMathChain
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentExecutor
import chainlit as cl

# Load environment variables from .env file
import os
from dotenv import load_dotenv
load_dotenv()

# Read Config
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# Set LLM Cache to optimize costs & speed up inference
from langchain.cache import SQLiteCache, RedisSemanticCache
from langchain.callbacks import get_openai_callback # TODO: Use this to get costs
import langchain
langchain.llm_cache = SQLiteCache(database_path="./cache/.llm.db") # TODO: Replace this with RedisSemanticCache


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
from langchain.schema import  HumanMessage, AIMessage, ChatMessage, FunctionMessage, SystemMessage
from langchain.llms import OpenAI

## Import all the tools
from MergeDevAgents import *
from Utilities import *
from UserAgents import *
from langchain.memory import ConversationBufferWindowMemory, ConversationKGMemory, ChatMessageHistory
from langchain.tools.human.tool import HumanInputRun

# TODO: 
# 1. Enable Streaming support - for masking latency
# 2. Incorporate Fallbacks - for robustness
# 3. Integrate with Langsmith - For logging and debugging

#####

class TopLevelAgent:
    def __init__(self, config):
        self.config = config
        self.tools = [HRISAgent(), PersonalInfoAgent(), CRMAgent()] # TODO: Also, add th KnowledgeGraphAgent here
        self.responsible_ai_agent = ResponsibleAIAgent()
        self.synthesis_agent = SynthesisAgent(config)
        self.history = ChatMessageHistory()
        self.kgLLM = OpenAI(model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1000) # TODO: Move to config

        # We use ReACT + CoT prompting methodology for this advanced reasoning agent
        self.ai_agent = initialize_agent(self.tools,
                    # TODO: We need an advanced LLM here that follows the instructions diligently. So, we use GPT-4 here.
                    ChatOpenAI(model="gpt-4-0613", temperature=0, max_tokens=1000),
                    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, # ReACT agent is best suited for this task.
                    verbose=True, # TODO: Config
                    memory=ConversationBufferWindowMemory(buffer_size=2)
                    )
                                         
    def run(self, utterance: str, cb: cl.LangchainCallbackHandler):
        # Perform Responsible AI Checks
        if (self.responsible_ai_agent.shouldFlag(utterance)):
            return "Your ask violates Responsible AI guidelines. Please rephrase your ask."

        if (self.responsible_ai_agent.detectPromptInjection(utterance)):
            return "Your ask violates Responsible AI guidelines. Please rephrase your ask."

        self.history.add_user_message(utterance)
        agent_response = self.ai_agent.run(utterance, callbacks=[cb])

        # We are using custom Synthesis agent instead of a Output Parser in order to keep the output more natural.
        response_to_user = self.synthesis_agent.run(utterance, agent_response)
        self.history.add_ai_message(response_to_user)
        return response_to_user


@cl.on_chat_start
async def start():
    msg = cl.Message(content="Hello! How can I help you today?")
    await msg.send()
    top_level_agent = TopLevelAgent(config)
    cl.user_session.set("agent", top_level_agent)

@cl.on_message
async def on_message(message: cl.Message):
    top_level_agent = cl.user_session.get("agent")
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)
    response = top_level_agent.run(message.content, cb)
    msg = cl.Message(content=response)
    await msg.send()
