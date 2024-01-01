import chainlit as cl

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Read Config
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# Set LLM Cache to optimize costs & speed up inference
from langchain.cache import SQLiteCache, RedisSemanticCache
import langchain
langchain.llm_cache = SQLiteCache(database_path="./cache/.llm.db") # TODO: Replace this with RedisSemanticCache

### A general principle I follow while architecting LLM solution is as follows:
### 1. Use LLM only for complex reasoning tasks. For simple tasks, write the algorithm or use traditional ML models directly.
### 2. A single LLM must be given a task that you think an untrained-human can perform the task by reading at most 1 page of instructions.
### 3. If the task is complex, break it down into multiple tasks and use multiple LLMs.

### In many cases, Langchain abstractions take you away from the LLM, thus losing finer control over them. This is necessary for a scalable and debuggable design.
### However, Langchain has an amazing array of tools and abstractions. We leverage Langchain but try to keep our control over LLMs completely.

from MergeDevAgents import *
from Utilities import *
from UserAgents import *
from langchain.memory import ConversationBufferWindowMemory, ConversationKGMemory, ChatMessageHistory

from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.tools import HumanInputRun

from TopLevelAgent import TopLevelAgent

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


# TODO: 
# 1. Incorporate Fallbacks - for robustness
# 2. Integrate with Langsmith - For logging and debugging
#####
