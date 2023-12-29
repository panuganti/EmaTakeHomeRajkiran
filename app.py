import chainlit as cl

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig


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

@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(streaming=True)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a very helpful agent.",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    top_level_agent = TopLevelAgent(config)
    response = top_level_agent.run(message.content)
    msg = cl.Message(content=response)
    await msg.send()
