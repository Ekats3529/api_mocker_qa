from services.base_service import BaseService
import allure


class TodosService(BaseService):
    def __init__(self):
        super().__init__("/todos")

    @allure.step("Получить все Todos с фильтрацией и пагинацией")
    def get_all_todos(self, user_id=None, completed=None, page=1, limit=10):
        params = {
            "_page": page,
            "_limit": limit
        }
        if user_id is not None:
            params["userId"] = user_id
        if completed is not None:
            params["completed"] = str(completed).lower()

        return self.request("GET", self.endpoint, params=params)
