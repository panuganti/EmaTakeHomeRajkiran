import merge
from merge.client import Merge
import os
from merge.resources.ats.types import CategoriesEnum
from merge.resources.ticketing.types import TicketStatusEnum

class MergeClient:
    def __init__(self):
        self.client = Merge(api_key=os.getenv("MERGEDEV_API_KEY"), account_token=os.getenv("YOUR_ACCOUNT_TOKEN"))

    def create_link_token(self):
        link_token_response = self.client.ats.link_token.create(
            end_user_email_address="john.smith@gmail.com",
            end_user_organization_name="acme",
            end_user_origin_id="1234",
            categories=[CategoriesEnum.ATS],
            link_expiry_mins=30,
        )
        return link_token_response.link_token

    def get_employee(self, id):
        employee = self.client.hris.employees.retrieve(id=id)
        return employee

    def get_candidate(self, id):
        candidate = self.client.ats.candidates.retrieve(id=id)
        return candidate

    def filter_candidates(self):
        candidates_response = self.client.ats.candidates.list(created_after="2030-01-01")
        return candidates_response.results

    def get_contact(self, id):
        contact = self.client.accounting.contacts.retrieve(id=id)
        return contact

    def create_ticket(self):
        self.client.ticketing.tickets.create(
            model=merge.ticketing.TicketRequest(
                name="Please add more integrations",
                assignees=[
                    "17a54124-287f-494d-965e-3c5b330c9a68"
                ],
                creator="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                due_date="2022-10-11T00:00:00Z",
                status=TicketStatusEnum.OPEN,
            ))

    def download_file(self, file_name, local_file_path):
        files = self.client.filestorage.files.list(name=file_name).results
        id = files[0].id
        name = files[0].name
        local_filename = f"{local_file_path}/{name}"
        response = self.client.filestorage.files.download_retrieve(id=id)
        with open(local_filename, "wb") as f:
            for chunk in response:
                f.write(chunk)

    def handle_pagination(self):
        response = self.client.hris.employees.list(created_after="2030-01-01")
        while response.next is not None:
            response = self.client.hris.employees.list(cursor=response.next, created_after="2030-01-01")
        return response
