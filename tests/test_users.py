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

    @allure.title("GET: Получение пользователя с {user_id}")
    @pytest.mark.parametrize("user_id", [2, 6, 9])
    def test_get_user_by_id(self, user_id):
        response = self.service.get_by_id(user_id)
        assert response.status_code == 200
        assert response.json()["data"]['id'] == user_id

    @allure.title("PUT: Полное обновление пользователя с ID {user_id}")
    @pytest.mark.parametrize("user_id", [2])
    def test_update_user(self, user_id):
        payload = {
            "name": "Updated Name",
            "username": "updated_user",
            "email": "updated@example.com"
        }
        response = self.service.update(user_id, payload)
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Updated Name"

    @allure.title("PATCH: Частичное обновление (email) пользователя с ID {user_id}")
    @pytest.mark.parametrize("user_id", [2])
    def test_patch_user(self, user_id):
        payload = {"email": "patch_test@example.com"}
        response = self.service.patch(user_id, payload)
        assert response.status_code == 200
        assert response.json()["data"]["email"] == payload["email"]

    @allure.title("DELETE: Удаление пользователя с ID {user_id}")
    @pytest.mark.parametrize("user_id", [16])
    def test_delete_user(self, user_id):
        response = self.service.delete(user_id)
        assert response.status_code in [200, 202, 204]
