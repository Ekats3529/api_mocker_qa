from services.base_service import BaseService
import allure
import logging


logger = logging.getLogger(__name__)


class UsersService(BaseService):
    def __init__(self):
        super().__init__("/users")

    @allure.step("Поиск пользователей по строке: {query}")
    def search(self, query):
        return self.request("GET", f"{self.endpoint}/search", params={"q": query})
