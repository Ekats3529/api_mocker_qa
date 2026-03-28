from services.base_service import BaseService
import allure
import logging


logger = logging.getLogger(__name__)


class UsersService(BaseService):
    def __init__(self):
        super().__init__("/users")

    def get_user_posts(self, user_id, page=1, limit=10):
        params = {"_page": page, "_limit": limit}
        return self.request("GET", f"{self.endpoint}/{user_id}/posts", params=params)

    def get_user_todos(self, user_id, page=1, limit=10):
        params = {"_page": page, "_limit": limit}
        return self.request("GET", f"{self.endpoint}/{user_id}/todos", params=params)
