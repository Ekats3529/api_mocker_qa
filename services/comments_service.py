from services.base_service import BaseService
import allure


class CommentsService(BaseService):
    def __init__(self):
        super().__init__("/comments")

    @allure.step("Получить все комментарии с фильтрацией и поиском")
    def get_all_comments(self, post_id=None, name_like=None, email_like=None, page=1, limit=10):

        params = {
            "_page": page,
            "_limit": limit
        }
        if post_id:
            params["postId"] = post_id
        if name_like:
            params["name_like"] = name_like
        if email_like:
            params["email_like"] = email_like

        return self.request("GET", self.endpoint, params=params)
