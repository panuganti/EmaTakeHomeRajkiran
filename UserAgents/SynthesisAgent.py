from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain

from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage # delete ?
from Utilities import *

import openai

# In many cases, this agent is not needed. 
# This is to be used only if we want to have a finer control over the UI elements and language used to present the response to the user. 
# TODO: Identify and plug-in relevant UI elements to be triggered based on the ask and the response.

class SynthesisAgent():
    name = "SynthesisAgent"
    description = "The SynthesisAgent is to be used Always for generating the output to the user. \
        It will select the appropriate UI elements and language to be presented to the user."

    def __init__(self, config):
        self.responsible_ai_agent = ResponsibleAIAgent()
        self.config = config
        self.llm = ChatOpenAI(model="gpt-4-0613", temperature=0, max_tokens=1000)
        
    def run(self, resolved_user_utterance, agent_response: str):
        # Perform Responsible AI Checks
        if (self.responsible_ai_agent.shouldFlag(agent_response)):
            return "I'm sorry, the response to your message violates our Responsible AI guidelines. Please ask for something else"

        # TODO: Add some message history here to make the response more relevant and natural
        system_message = f"""
            You are a helpful AI bot. Your task is to answer user's question with very specific relevant information to the question in a natural way. \
            Do not provide any information that is not explicitly asked for. \ 

            The user is, which is delimited by triple backticks, provide the answer strictly from the content, which is delimited by triple hashes. \
            In case the content is about asking the user for clarification, your task is to ask the user for clarification. \ 
            ```{resolved_user_utterance}```
            ### {agent_response} ###
            """
        
        prompt = PromptTemplate(input_variables=[resolved_user_utterance, agent_response], 
                                template=system_message)
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain({'resolved_user_utterance': resolved_user_utterance}, 
                         {'agent_response': agent_response})
        return response['text']
