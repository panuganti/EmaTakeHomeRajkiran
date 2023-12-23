# from autogen import autogen
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
import os

# Load environment variables from .env file
from dotenv import load_dotenv, dotenv_values, set_key
load_dotenv()

# Read the configuration file
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Define the agent
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage

# App Logic
from NativeAgents.TopLevelAgent import TopLevelAgent
top_level_agent = TopLevelAgent(config)

# Quick UI
import streamlit as st
st.set_page_config(page_title="Enterprise Copilot")
st.header("Enterprise Copilot")
input = st.text_input("Enter your message here", "Your question goes here ...")
submit = st.button("Submit")
if submit:
    st.write("You: " + input)
    response = top_level_agent.ProcessUserTask(input)
    st.write("Bot:" + response)




