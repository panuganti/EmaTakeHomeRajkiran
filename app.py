import chanlit as cl
# Load environment variables from .env file
# import os
# from dotenv import load_dotenv
# load_dotenv()

# Set LLM Cache to optimize costs & speed up inference
from langchain.cache import SQLiteCache, RedisSemanticCache
from langchain.callbacks import get_openai_callback # TODO: Use this to get costs
import langchain
langchain.llm_cache = SQLiteCache(database_path="./cache/.llm.db") # TODO: Replace this with RedisSemanticCache

# Read Config
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

from NativeAgents import *

#@cl.on_message
def handle_message(message):
    top_level_agent = TopLevelAgent(config)
    # print(top_level_agent.run("What is my time off balance?"))
    # response = top_level_agent.run("Summarize my last conversation with Bill’s company")
    response = top_level_agent.run(message.content)
    cl.send_message(content=response)

    # top_level_agent.run("How many vacations do I have remaining?")
    # top_level_agent.run("What is the total HC cost for each of my managers?")
    # top_level_agent.run("How much revenue does the top 10 customers bring in?")
    # top_level_agent.run("What fraction of P0 bugs in my organization has been fixed within SLA?")
    # top_level_agent.run("How many leads have we not met yet?")
    # top_level_agent.run("Tell me the pending time off requests for my team members in Bangalore.")
    # top_level_agent.run("For my team in bangalore, tell me the count of tickets assigned to each of them, and how many rounds of interview they each had.")





