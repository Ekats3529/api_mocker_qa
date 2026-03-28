import requests
import allure
import logging

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"

        with allure.step(f"Отправка {method} запроса на {url}"):
            response = requests.request(method, url, **kwargs)

            logger.info(f"Request: {method} {url} | Status: {response.status_code}")
            allure.attach(f"URL: {url}", name="Request URL", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.status_code), name="Response Status",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

            return response