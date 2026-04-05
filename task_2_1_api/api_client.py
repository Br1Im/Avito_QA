"""API клиент для сервиса объявлений Авито."""

import requests


class APIClient:
    """Клиент для работы с API объявлений."""

    def __init__(self, base_url="https://qa-internship.avito.com"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        self.session.headers["Accept"] = "application/json"

    def create_item(self, body):
        """Создать объявление. POST /api/1/item"""
        return self.session.post(f"{self.base_url}/api/1/item", json=body)

    def get_item_by_id(self, item_id):
        """Получить объявление по ID. GET /api/1/item/:id"""
        return self.session.get(f"{self.base_url}/api/1/item/{item_id}")

    def get_items_by_seller(self, seller_id):
        """Получить все объявления продавца. GET /api/1/:sellerId/item"""
        return self.session.get(f"{self.base_url}/api/1/{seller_id}/item")

    def get_statistic_v1(self, item_id):
        """Получить статистику v1. GET /api/1/statistic/:id"""
        return self.session.get(f"{self.base_url}/api/1/statistic/{item_id}")

    def delete_item(self, item_id):
        """Удалить объявление. DELETE /api/2/item/:id"""
        return self.session.delete(f"{self.base_url}/api/2/item/{item_id}")

    def get_statistic_v2(self, item_id):
        """Получить статистику v2. GET /api/2/statistic/:id"""
        return self.session.get(f"{self.base_url}/api/2/statistic/{item_id}")

    @staticmethod
    def extract_id(response):
        """Извлечь UUID из ответа создания. POST возвращает status: 'Создано - UUID'"""
        data = response.json()
        status_str = data.get("status", "")
        if " - " in status_str:
            return status_str.split(" - ", 1)[1].strip()
        return None

    def create_test_item(self, seller_id=111111, name="Test", price=1000, statistics=None):
        """Создать тестовое объявление с дефолтными значениями.
        API требует ненулевую статистику для всех трёх полей."""
        if statistics is None:
            statistics = {"likes": 10, "viewCount": 50, "contacts": 5}
        body = {
            "sellerID": seller_id,
            "name": name,
            "price": price,
            "statistics": statistics,
        }
        return self.create_item(body)

    def close(self):
        """Закрыть сессию."""
        self.session.close()
