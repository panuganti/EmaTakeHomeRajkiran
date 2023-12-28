from langchain.llms import OpenAI
from langchain.indexes import GraphIndexCreator
from langchain.chains import GraphQAChain
from langchain.prompts import PromptTemplate
from langchain_core.tools import BaseTool
from langchain.tools import Tool

# In this case, we are building knowledge graph from the knowledge we extract from the user's utterance to capture user's preferences.
# We do not add knowledge from the backend data. Hence, the data is never going to be stale.
# However, user's preference can change over time. Hence, we need to update the knowledge graph.

class KnowledgeGraphAgent():
    name = "custom_search"
    description = "The KnowledgeGraphAgent is used to query the knowledge graph for retrieving from user's preferences."

    def __init__(self):
        self.llm = OpenAI(model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1000) # TODO: Move to config
        self.graph_index_creator = GraphIndexCreator(llm=self.llm)
        self.knowledge_graph = self.graph_index_creator.from_text("") # Initialize empty graph

    def add_to_knowledge_graph(self, knowledge: str):
        """Extracts the knowledge from the input and adds it to the knowledge graph."""
        triples = self.graph_index_creator.from_text(knowledge)
        for (node1, relation, node2) in triples.get_triples():
            self.knowledge_graph.add_triple(node1, relation, node2)

    # If user corrects the assumption we made, we need to remove the triple from the knowledge graph
    # If there is an update to the knowledge, we need to update the knowledge graph
    def remove_from_knowledge_graph(self, knowledge: str):
        """Extracts the knowledge from the input and removes it from the knowledge graph."""
        triples = self.graph_index_creator.from_text(knowledge)
        for (node1, relation, node2) in triples.get_triples():
            self.knowledge_graph.delete_triple(node1, relation, node2)

    def query_knowledge_graph(self, query: str):
        """Queries the knowledge graph and returns the answer."""
        prompt = PromptTemplate(input_variables=[query], 
                                       template="What is the answer to the question: {query}? If you do not know the answer, please say 'I do not know'.")
        llm = OpenAI(model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1000) # TODO: Move to config
        chain = GraphQAChain(self.llm, prompt=prompt)
        response = chain({'query': query}, 
                         {'knowledge_graph': self.knowledge_graph})
        return response['text']
    
    def _run(self, query: str):
        """Runs the agent."""
        answer = self.query_knowledge_graph(query)
        return answer
    
    def _arun(self, query: str):
        """Runs the agent asynchronously."""
        raise NotImplementedError("This tool does not support async")