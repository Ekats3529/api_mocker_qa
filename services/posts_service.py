from services.base_service import BaseService
import allure


class PostsService(BaseService):
    def __init__(self):
        super().__init__("/posts")

    @allure.step("Получить все посты с фильтрацией и пагинацией")
    def get_all_posts(self, user_id=None, page=1, limit=10):
        params = {"_page": page, "_limit": limit}
        if user_id:
            params["userId"] = user_id
        return self.request("GET", self.endpoint, params=params)

    @allure.step("Получить лайки поста {post_id}")
    def get_likes(self, post_id):
        return self.request("GET", f"{self.endpoint}/{post_id}/likes")

    @allure.step("Добавление лайка посту {post_id} от пользователя {user_id}")
    def add_like(self, post_id, user_id=None):
        payload = {"userId": user_id} if user_id else {}
        return self.request("POST", f"{self.endpoint}/{post_id}/likes", json=payload)

