
class CRMAgent:
    def __init__(self, config):
        self.config = config

    def display(self):
        print(f"MyClassInSubdirectory value: {self.value}")


class MergeCRMMockAPI:
    def __init__(self):
        pass

    def get_accounts(self):
        return "Mock data for GET /accounts"

    def get_account_by_id(self, account_id):
        return f"Mock data for GET /accounts/{account_id}"

    def get_contacts(self):
        return "Mock data for GET /contacts"

    def get_contact_by_id(self, contact_id):
        return f"Mock data for GET /contacts/{contact_id}"

    def get_engagement_types(self):
        return "Mock data for GET /engagement-types"

    def get_engagement_type_by_id(self, engagement_type_id):
        return f"Mock data for GET /engagement-types/{engagement_type_id}"

    def get_engagements(self):
        return "Mock data for GET /engagements"

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
