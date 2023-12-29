from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage, FunctionMessage

from langchain.tools import BaseTool
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

class RecruitingAgent(BaseTool):
    name = "RecruitingAgent"
    description = "The RecruitingAgent is used to get information related to Recruiting. It takes input in a natural language format.\
                    The information broadly falls into the following categories. \
                    1. The Activity object is used to represent an activity for a candidate performed by a user.\
                    2. The Application Object is used to represent a candidate's journey through a particular Job's recruiting process. If a Candidate applies for multiple Jobs, there will be a separate Application for each Job if the third-party integration allows it.\
                    3. The Attachment object is used to represent a file attached to a candidate.\
                    4. The Candidate object is used to represent profile information about a given Candidate. Because it is specific to a Candidate, this information stays constant across applications.\
                    5. The Department object is used to represent a department within a company.\
                    6. The EEOC object is used to represent the Equal Employment Opportunity Commission information for a candidate (race, gender, veteran status, disability status).\
                    7. The ScheduledInterview object is used to represent a scheduled interview for a given candidate’s application to a job. An Application can have multiple ScheduledInterviews depending on the particular hiring process.\
                    8. The JobInterviewStage object is used to represent a particular recruiting stage for an Application. A given Application typically has the JobInterviewStage object represented in the current_stage field.\
                    9. The Job object can be used to track any jobs that are currently or will be open/closed for applications.\
                    10. The Offer object is used to represent an offer for a candidate's application specific to a job.\
                    11. The Office object is used to represent an office within a company. A given Job has the Office ID in its offices field.\
                    12. The RejectReason object is used to represent a reason for rejecting an application. These can typically be configured within an ATS system.\
                    13. The Scorecard object is used to represent an interviewer's candidate recommendation based on a particular interview.\
                    14. The ScreeningQuestion object is used to represent questions asked to screen candidates for a job.\
                    15. The Tag object is used to represent a tag for a candidate.\
                    16. The RemoteUser object is used to represent a user with a login to the ATS system.\
                    "

    def _run(self, utterance: str):
        tools = []
        ai_agent = initialize_agent(tools,
                            # The task here is straightforward. Hence, gpt-3.5-turbo is sufficient.
                            # For cost optimization, we can replace this agent with a combination of Intent-Detection & Entity/Slot Extraction
                            ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, cache=False),
                            agent=AgentType.OPENAI_FUNCTIONS,
                            handle_parsing_errors=True,
                            verbose=False)
        response = ai_agent.run(utterance)
        return response

    def _arun(self, utterance: str):
        raise NotImplementedError("This tool does not support async")


from merge.client import Merge

