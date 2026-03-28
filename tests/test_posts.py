import pytest
import allure
from services.posts_service import PostsService
import logging

logger = logging.getLogger(__name__)


@allure.suite("Тестирование Постов (Посты)")
class TestUsers:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = PostsService()

    @allure.title("GET: Получение списка всех постов")
    def test_get_all_posts(self):
        response = self.service.get_all()
        assert response.status_code == 200
        assert isinstance(response.json()['data'], list)

    @allure.title("GET: Получение всех постов с фильтром по userId и пагинацией")
    def test_get_posts_with_pagination(self):
        user_id, page, limit = 6, 1, 5
        response = self.service.get_all_posts(user_id=user_id, page=page, limit=limit)

        assert response.status_code == 200
        json_data = response.json()

        assert "data" in json_data
        assert "pagination" in json_data
        assert json_data['data'][0]['userId'] == user_id
        assert json_data['pagination']['total'] > 0

    @allure.title("POST: Создание нового поста")
    def test_create_post(self):
        payload = {
            "title": "New Post Title 1",
            "body": "This is the content of the new post 1..."
        }
        response = self.service.create(payload)

        logger.info(response.json())

        assert response.status_code in [200, 201]
        assert response.json()["data"]["title"] == payload["title"]
        assert response.json()["data"]["userId"] == 1

    @allure.title("GET: Получение лайков поста")
    def test_get_post_likes(self):
        post_id = 13
        response = self.service.get_likes(post_id)

        assert response.status_code == 200
        assert response.json()["postId"] == post_id
        assert "likes" in response.json()

    @allure.title("POST: Добавление лайка посту (анонимно и от юзера)")
    @pytest.mark.parametrize("user_id", [None, 1])
    def test_add_like_to_post(self, user_id):
        post_id = 13
        response = self.service.add_like(post_id, user_id=user_id)

        assert response.status_code in [200, 201]
        assert response.json()["message"] == "Like added successfully"
        assert "totalLikes" in response.json()

    @allure.title("DELETE: Удаление поста")
    def test_delete_post(self):
        response = self.service.delete(23)
        assert response.status_code in [200, 204]


