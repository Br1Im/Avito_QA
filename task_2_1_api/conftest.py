"""Фикстуры для API тестов."""

import random
import pytest
from api_client import APIClient


@pytest.fixture(scope="session")
def base_url():
    return "https://qa-internship.avito.com"


@pytest.fixture
def api_client(base_url):
    """Создаёт API клиент для каждого теста."""
    client = APIClient(base_url)
    yield client
    client.close()


@pytest.fixture
def unique_seller_id():
    """Генерирует уникальный seller ID в диапазоне 111111-999999."""
    return random.randint(111111, 999999)


@pytest.fixture
def created_item(api_client, unique_seller_id):
    """Создаёт тестовое объявление и возвращает ответ и seller_id."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Тестовое объявление",
        price=1000,
    )
    return response, unique_seller_id
