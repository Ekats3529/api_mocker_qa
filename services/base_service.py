from core.api_client import APIClient
import allure
import logging


logger = logging.getLogger(__name__)


class BaseService(APIClient):
    def __init__(self, resource_path):
        base_url = "https://apimocker.com"
        super().__init__(base_url)
        self.endpoint = resource_path

    def get_all(self):
        return self.request("GET", self.endpoint)

    def get_by_id(self, item_id):
        return self.request("GET", f"{self.endpoint}/{item_id}")

    def create(self, data):
        return self.request("POST", self.endpoint, json=data)

    def update(self, item_id, data):
        return self.request("PUT", f"{self.endpoint}/{item_id}", json=data)

    def patch(self, item_id, data):
        return self.request("PATCH", f"{self.endpoint}/{item_id}", json=data)

    def delete(self, item_id):
        return self.request("DELETE", f"{self.endpoint}/{item_id}")
