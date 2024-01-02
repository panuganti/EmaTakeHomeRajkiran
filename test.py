### A general principle I follow while architecting LLM solution is as follows:
### 1. Use LLM only for complex reasoning tasks. For simple tasks, write the algorithm or use traditional ML models directly.
### 2. A single LLM must be given a task that you think an untrained-human can perform the task by reading at most 1 page of instructions.
### 3. If the task is complex, break it down into multiple tasks and use multiple LLMs.

### In many cases, Langchain abstractions take you away from the LLM, thus losing finer control over them. This is necessary for a scalable and debuggable design.
### However, Langchain has an amazing array of tools and abstractions. We leverage Langchain but try to keep our control over LLMs completely.

# TODO: 
# 1. Incorporate Fallbacks - for robustness
# 2. Integrate with Langsmith - For logging and debugging
#####

###########################

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


from TopLevelAgent import TopLevelAgent
top_level_agent = TopLevelAgent(config)
response = top_level_agent.run("What's my time off balance ?", None)


#################### TOP LEVEL AGENT ####################
## Import all the tools
# from MergeDevAgents import *
# from Utilities import *
# from UserAgents import *
# from langchain.memory import ConversationBufferWindowMemory, ConversationKGMemory, ChatMessageHistory

# from langchain.agents import AgentType, initialize_agent
# from langchain.chat_models import ChatOpenAI
# from langchain.llms import OpenAI
# from langchain.tools import HumanInputRun

# tools = [HumanInputRun(), HRISAgent(), PersonalInfoAgent(), CRMAgent()] # TODO: Also, add th KnowledgeGraphAgent here
# responsible_ai_agent = ResponsibleAIAgent()
# synthesis_agent = SynthesisAgent(config)
# history = ChatMessageHistory()
# kgLLM = OpenAI() # TODO: Move to config

# # We use ReACT + CoT prompting methodology for this advanced reasoning agent
# llm = ChatOpenAI(temperature=0.0)
# ai_agent = initialize_agent(
#             tools,
#             llm,
#             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # ReACT agent is best suited for this task.
#             verbose=True, # TODO: Config
#             memory=ConversationBufferWindowMemory(buffer_size=2)
#             )

# ai_agent.run("What's my time off balance ?")
# print("Hello! How can I help you today?")

# while True:
#     utterance = input("Enter your ask:\n")
#     if (utterance == "exit"):
#         break

#     if responsible_ai_agent.shouldFlag(utterance) or responsible_ai_agent.detectPromptInjection(utterance):
#         print("Your ask violates Responsible AI guidelines. Please rephrase your ask.")
    
#     history.add_user_message(utterance)
#     agent_response = ai_agent.run(utterance)
#     response_to_user = synthesis_agent.run(utterance, agent_response)
#     history.add_ai_message(response_to_user)


