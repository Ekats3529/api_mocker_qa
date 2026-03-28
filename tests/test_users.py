import pytest
import allure
from services.users_service import UsersService
import logging

logger = logging.getLogger(__name__)


@allure.suite("Тестирование Пользователей (Users)")
class TestUsers:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = UsersService()

    @allure.title("GET: Получение списка всех пользователей")
    def test_get_users(self):
        response = self.service.get_all()
        assert response.status_code == 200
        assert isinstance(response.json()['data'], list)

    @allure.title("GET: Получение пользователя с ID {user_id}")
    @pytest.mark.parametrize("user_id", [2, 6, 9])
    def test_get_user_by_id(self, user_id):
        response = self.service.get_by_id(user_id)
        assert response.status_code == 200
        assert response.json()["data"]['id'] == user_id

    @allure.title("POST: Создание нового пользователя")
    def test_create_user(self):
        payload = {
            "name": "Leanne Graham",
            "username": "Bret__GR",
            "email": "Sincere_1@apppril.biz"
        }
        response = self.service.create(payload)

        # Обычно API возвращает 201 Created при создании
        assert response.status_code in [200, 201]
        assert response.json()["data"]["name"] == payload["name"]
        assert "id" in response.json()["data"]

    @allure.title("PUT: Полное обновление пользователя с ID {user_id}")
    @pytest.mark.parametrize("user_id", [2])
    def test_update_user(self, user_id):
        payload = {
            "id": user_id,
            "name": "Updated Name",
            "username": "updated_user",
            "email": "updated@example.com"
        }
        response = self.service.update(user_id, payload)

        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Updated Name"
        assert response.json()["data"]["email"] == "updated@example.com"

    @allure.title("DELETE: Удаление пользователя с ID {user_id}")
    @pytest.mark.parametrize("user_id", [22])
    def test_delete_user(self, user_id):
        response = self.service.delete(user_id)
        assert response.status_code in [200, 202, 204]

    @allure.title("GET: Получить посты пользователся с ID {user_id}")
    @pytest.mark.parametrize("user_id", [6])
    def test_get_user_posts(self, user_id):
        page, limit = 1, 5
        response = self.service.get_user_posts(user_id, page=page, limit=limit)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data['data'], list)
        assert data['pagination']['page'] == page
        assert data['pagination']['limit'] == limit

    @allure.title("GET: Получение задач пользователя с ID {user_id}")
    def test_get_user_todos(self):
        response = self.service.get_user_todos(user_id=2)
        assert response.status_code == 200
        assert "data" in response.json()
