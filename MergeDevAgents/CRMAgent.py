import datetime
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import json
from pydantic import BaseModel, Field

class CRMAgent(BaseTool):
    name = "CRM Agent"
    description = "The CRM Agent tool used to retrieve information related to Contacts, Companies, Accounts, Engagements or Conversations. I take input in a natural language format."

    def _run(self, utterance: str):
        tools = [CRMContactsTool(), CRMEngagementsTool()]
        ai_agent = initialize_agent(tools,
                            # The task here is straightforward. Hence, gpt-3.5-turbo is sufficient.
                            # For cost optimization, we can replace this agent with a combination of Intent-Detection & Entity/Slot Extraction
                            ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, cache=False),
                            agent=AgentType.OPENAI_FUNCTIONS,
                            handle_parsing_errors=True,
                            verbose=True)
        response = ai_agent.run(utterance)
        return response

    def _arun(self, utterance: str):
        raise NotImplementedError("This tool does not support async")

# Define a custom JSON encoder for the Contact class
class ContactEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Contact):
            return {
                'name': obj.name,
                'contact_id': obj.contact_id,
                'account_id': obj.account_id,
            }
        return super().default(obj)

class Contact:
    def __init__(self, contact_id: str, name: str, account_id: str):
        self.contact_id = contact_id
        self.name = name
        self.account_id = account_id

class CRMCheckInput(BaseModel):
    """Input for retrieving account related information."""

    name: str = Field(..., description="Name")

class EngaegmentCheckInput(BaseModel):
    """Input for retrieving engaegment related information."""

    account_id: str = Field(..., description="Account Id")

class CRMContactsTool(BaseTool):
    name = "get_contacts"
    description = "The Contacts object is used to represent the information about a person including their company information. The account_id represents the company of the person."

    def _run(self, name: str):
        crm = CRM()
        contacts = crm.get_contacts(name)
        contacts_json = json.dumps(contacts, cls=ContactEncoder)
        return contacts_json

    def _arun(self, name: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = CRMCheckInput

class CRMEngagementsTool(BaseTool):
    name = "get_engagements"
    description = "The Engagements object is used to represent the conversation with a person of a company. The account_id represents the company of the person."

    def _run(self, account_id: str):
        crm = CRM()
        engagements = crm.get_engagements(account_id)
        engagements_json = json.dumps(engagements, cls=EngagementEncoder)
        return engagements_json

    def _arun(self, account_id: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Type[BaseModel] = EngaegmentCheckInput

class Account:
    def __init__(self, account_id: str, name: str):
        self.account_id = account_id
        self.name = name

# Define a custom JSON encoder for the Engagement class
class EngagementEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Engagement):
            return {
                'owner': obj.owner,
                'content': obj.content,
                'subject': obj.subject,
                'direction': obj.direction,
                'engagement_type_id': obj.engagement_type_id,
                'start_time': obj.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'account_id': obj.account_id,
                'contacts': obj.contacts,
            }
        return super().default(obj)

class Engagement:
    def __init__(self, owner: str, content: str, subject: str, direction: str, 
                 engagement_type_id: str, start_time: datetime, id: str, 
                 account_id: str, contacts: list[str] ):
        self.owner = owner
        self.content = content
        self.subject = subject
        self.direction = direction
        self.engagement_type_id = engagement_type_id
        self.start_time = start_time
        self.id = id
        self.account_id = account_id
        self.contacts = contacts


class CRM:
    def __init__(self):
        self.mock_accounts = [
            Account("account_id_1", "Acme Inc."),
            Account("account_id_2", "Globex Corp."),
            Account("account_id_3", "Soylent Corp.")
        ]
        self.mock_contacts = [
            Contact("contact_id_1", "Bill Gates", "account_id_1"),
            Contact("contact_id_1", "Bill Clinton", "account_id_2"),
            Contact("contact_id_2", "Jane Doe", "account_id_1"),
            Contact("contact_id_3", "Steve Smith", "account_id_2")
        ]

        mock_email = "I hope this email finds you well. I wanted to touch base regarding our upcoming team meeting scheduled for [Date and Time]. As we prepare for the meeting, I wanted to share the agenda and some important updates.\ Agenda for the Meeting:\
                        1. **Opening Remarks**: Brief introduction and welcome.\
                        2. **Review of Previous Meeting Minutes**: Recap of key points from our last meeting. \
                        3. **Project Updates**: A discussion of ongoing projects and milestones achieved. \
                        4. **Upcoming Deadlines**: A reminder of important deadlines and deliverables. \
                        5. **Team Collaboration**: An opportunity to discuss any challenges or successes in our teamwork.\ Thank you for your continued dedication and hard work."

        self.mock_engagements = [
            Engagement("John Doe", "This is the content of the engagement", "This is the subject of the engagement", "INCOMING", "engagement_type_id_1", 
                       datetime.datetime(2023, 12, 16, 12, 12, 12), "id_1", "account_id_1", ["contact_id_1", "contact_id_2"]),
            Engagement("Christine", mock_email, "Re: Try our product", "INCOMING", "engagement_type_id_2", 
                       datetime.datetime(2023, 12, 17, 12, 12, 12), "id_2", "account_id_1", ["John Doe", "Bill"]),
            Engagement("John Doe", "This is the content of the engagement", "This is the subject of the engagement", "INCOMING", "engagement_type_id_3", 
                       datetime.datetime(2023, 12, 18, 12, 12, 12), "id_3", "account_id_2", ["contact_id_1", "contact_id_2"]),
            Engagement("John Doe", "This is the content of the engagement", "This is the subject of the engagement", "INCOMING", "engagement_type_id_4", 
                       datetime.datetime(2023, 12, 19, 12, 12, 12), "id_4", "account_id_3", ["contact_id_1", "contact_id_2"]),
        ]

    def get_accounts(self, query):
        return self.mock_data # Mock Data

    def get_account_by_id(self, account_id):
        return [account for account in self.mock_accounts if account.account_id == account_id]

    def get_engagements(self, account_id):
        return [engagement for engagement in self.mock_engagements if engagement.account_id == account_id]

    def get_contacts(self, name):
        return [contact for contact in self.mock_contacts if contact.name.startswith(name)]
    
    def get_contact_by_id(self, contact_id):
        return f"Mock data for GET /contacts/{contact_id}"

    def get_engagement_types(self):
        return "Mock data for GET /engagement-types"

    def get_engagement_type_by_id(self, engagement_type_id):
        return f"Mock data for GET /engagement-types/{engagement_type_id}"

    def get_engagement_by_id(self, engagement_id):
        return f"Mock data for GET /engagements/{engagement_id}"

    def get_leads(self):
        return "Mock data for GET /leads"

    def get_lead_by_id(self, lead_id):
        return f"Mock data for GET /leads/{lead_id}"

    def get_notes(self):
        return "Mock data for GET /notes"

    def get_note_by_id(self, note_id):
        return f"Mock data for GET /notes/{note_id}"

    def get_opportunities(self):
        return "Mock data for GET /opportunities"

    def get_opportunity_by_id(self, opportunity_id):
        return f"Mock data for GET /opportunities/{opportunity_id}"

    def get_stages(self):
        return "Mock data for GET /stages"

    def get_stage_by_id(self, stage_id):
        return f"Mock data for GET /stages/{stage_id}"

    def get_tasks(self):
        return "Mock data for GET /tasks"

    def get_task_by_id(self, task_id):
        return f"Mock data for GET /tasks/{task_id}"

    def get_users(self):
        return "Mock data for GET /users"

    def get_user_by_id(self, user_id):
        return f"Mock data for GET /users/{user_id}"

    def get_custom_object_classes(self):
        return "Mock data for GET /custom-object-classes"

    def get_custom_object_class_by_id(self, custom_object_class_id):
        return f"Mock data for GET /custom-object-classes/{custom_object_class_id}"

    # Additional methods for other GET endpoints can be added here



