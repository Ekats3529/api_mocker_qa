import pytest
import allure
import random
from services.comments_service import CommentsService
import logging

logger = logging.getLogger(__name__)


@allure.suite("Тестирование Комментариев (Comments)")
class TestComments:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = CommentsService()

    @allure.title("GET: Получение списка всех комментариев")
    def test_get_all_comments(self):
        response = self.service.get_all()
        assert response.status_code == 200
        assert isinstance(response.json()['data'], list)

    @allure.title("GET: Все комментарии с поиском по имени и пагинацией")
    def test_get_comments_with_search(self):
        name_query = "John"
        response = self.service.get_all_comments(name_like=name_query, page=1, limit=5)

        assert response.status_code == 200
        res_body = response.json()

        assert "data" in res_body
        assert res_body["pagination"]["limit"] == 5

        if res_body["data"]:
            assert name_query.lower() in res_body["data"][0]["name"].lower()

    @allure.title("GET: Получение комментария с ID {comment_id}")
    @pytest.mark.parametrize("comment_id", [61])
    def test_get_comments_by_id(self, comment_id):
        response = self.service.get_by_id(comment_id)
        assert response.status_code == 200
        assert response.json()["data"]['id'] == comment_id

    @allure.title("POST: Создание нового комментария")
    def test_create_comment(self):
        payload = {
            "name": "Example",
            "email": f"test_{random.randint(1, 999)}@example.com",
            "body": "Example",
            "postId": 1
        }
        response = self.service.create(payload)
        logger.info(response.json())

        assert response.status_code in [200, 201]
        assert response.json()["data"]["email"] == payload["email"]
        assert response.json()["data"]["postId"] == 1

    @allure.title("PUT: Обновление комментария")
    def test_update_comment(self):
        comment_id = 64
        payload = {
            "body": "Updated comment body content"
        }
        response = self.service.update(comment_id, payload)
        logger.info(response.json())

        assert response.status_code == 200
        assert response.json()["data"]["body"] == payload["body"]

    @allure.title("DELETE: Удаление комментария")
    @pytest.mark.parametrize("comment_id", [71])
    def test_delete_comment(self, comment_id):
        response = self.service.delete(comment_id)
        assert response.status_code in [200, 204]
