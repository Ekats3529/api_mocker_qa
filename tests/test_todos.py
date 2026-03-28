import pytest
import allure
from services.todos_service import TodosService
import logging
import random

logger = logging.getLogger(__name__)


@allure.suite("Тестирование Задач (Todos)")
class TestTodos:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = TodosService()

    @allure.title("GET: Получение списка всех todos")
    def test_get_all_todos(self):
        response = self.service.get_all()
        assert response.status_code == 200
        assert isinstance(response.json()['data'], list)

    @allure.title("GET: Получение всех задач с фильтрацией по userId и статусу completed")
    def test_get_todos_with_filters(self):
        user_id, completed, page, limit = 6, True, 1, 5
        response = self.service.get_all_todos(
            user_id=user_id,
            completed=completed,
            page=page,
            limit=limit
        )

        assert response.status_code == 200
        res_body = response.json()

        assert res_body["pagination"]["limit"] == limit

        if res_body["data"]:
            assert res_body["data"][0]["userId"] == user_id
            assert res_body["data"][0]["completed"] is True

    @allure.title("GET: Получение задачи по ID")
    @pytest.mark.parametrize("todo_id", [22])
    def test_get_todo_by_id(self, todo_id):
        response = self.service.get_by_id(todo_id)
        assert response.status_code == 200
        assert response.json()["data"]["id"] == todo_id

    @allure.title("POST: Создание новой задачи")
    def test_create_todo(self):
        unique_title = f"Task {random.randint(1000, 9999)}"
        payload = {
            "title": unique_title,
        }
        response = self.service.create(payload)

        logger.info(response.json())

        assert response.status_code in [200, 201]
        assert response.json()["data"]["title"] == unique_title
        assert response.json()["data"]["completed"] is False

    @allure.title("PUT: Полное обновление задачи")
    @pytest.mark.parametrize("todo_id", [23])
    def test_update_todo(self, todo_id):
        payload = {
            "title": "Updated Title"
        }
        response = self.service.update(todo_id, payload)

        logger.info(response.json())

        assert response.status_code == 200
        assert response.json()["data"]["completed"] is True

    @allure.title("DELETE: Удаление задачи")
    @pytest.mark.parametrize("todo_id", [32])
    def test_delete_todo(self, todo_id):
        response = self.service.delete(todo_id)
        assert response.status_code in [200, 204]