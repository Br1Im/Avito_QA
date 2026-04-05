"""Позитивные тесты API."""

import allure
import pytest
from api_client import APIClient


@allure.title("TC-001: Создание объявления с валидными данными")
@pytest.mark.positive
def test_create_item_valid_data(api_client, unique_seller_id):
    """Проверяем, что создание объявления с валидными данными возвращает 200."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Тест",
        price=1000,
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["sellerId"] == unique_seller_id
    assert data["name"] == "Тест"
    assert data["price"] == 1000
    assert data["statistics"]["likes"] == 0


@allure.title("TC-002: Создание объявления с ценой 0")
@pytest.mark.positive
def test_create_item_min_price(api_client, unique_seller_id):
    """Проверяем, что цена 0 принимается."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Бесплатно",
        price=0,
    )
    assert response.status_code == 200
    assert response.json()["price"] == 0


@allure.title("TC-003: Создание объявления с максимальной ценой")
@pytest.mark.positive
def test_create_item_max_price(api_client, unique_seller_id):
    """Проверяем большую цену."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Дорого",
        price=999999999,
    )
    assert response.status_code == 200
    assert response.json()["price"] == 999999999


@allure.title("TC-004: Создание объявления с пустой статистикой")
@pytest.mark.positive
def test_create_item_empty_statistics(api_client, unique_seller_id):
    """Проверяем инициализацию статистики нулями."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Без статистики",
        price=100,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["statistics"]["likes"] == 0
    assert data["statistics"]["viewCount"] == 0
    assert data["statistics"]["contacts"] == 0


@allure.title("TC-005: Создание объявления со статистикой")
@pytest.mark.positive
def test_create_item_with_statistics(api_client, unique_seller_id):
    """Проверяем сохранение ненулевой статистики."""
    stats = {"likes": 10, "viewCount": 50, "contacts": 5}
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Популярное",
        price=5000,
        statistics=stats,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["statistics"]["likes"] == 10
    assert data["statistics"]["viewCount"] == 50
    assert data["statistics"]["contacts"] == 5


@allure.title("TC-006: Несколько объявлений одного продавца")
@pytest.mark.positive
def test_create_multiple_items_same_seller(api_client, unique_seller_id):
    """Создаём 3 объявления и проверяем, что все сохраняются."""
    for i in range(3):
        response = api_client.create_test_item(
            seller_id=unique_seller_id,
            name=f"Объявление {i}",
            price=100 * (i + 1),
        )
        assert response.status_code == 200

    response = api_client.get_items_by_seller(unique_seller_id)
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 3


@allure.title("TC-007: Разные продавцы получают разные ID")
@pytest.mark.positive
def test_unique_ids_for_different_sellers(api_client):
    """Проверяем, что у разных продавцов разные ID объявлений."""
    response1 = api_client.create_test_item(seller_id=222222, name="Продавец 1", price=100)
    response2 = api_client.create_test_item(seller_id=333333, name="Продавец 2", price=200)
    assert response1.status_code == 200
    assert response2.status_code == 200
    id1 = response1.json()["id"]
    id2 = response2.json()["id"]
    assert id1 != id2


@allure.title("TC-008: Кириллическое название")
@pytest.mark.positive
def test_create_item_cyrillic_name(api_client, unique_seller_id):
    """Проверяем, что кириллица сохраняется корректно."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Персидский котёнок",
        price=5000,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Персидский котёнок"
