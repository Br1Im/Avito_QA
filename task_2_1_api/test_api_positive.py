"""Позитивные тесты API."""

import allure
import pytest


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
    item_id = api_client.extract_id(response)
    assert item_id is not None
    item_data = api_client.get_item_by_id(item_id)
    assert item_data.status_code == 200
    data = item_data.json()[0]
    assert data["sellerId"] == unique_seller_id
    assert data["name"] == "Тест"
    assert data["price"] == 1000
    assert data["statistics"]["likes"] == 10


@allure.title("TC-003: Создание объявления с большой ценой")
@pytest.mark.positive
def test_create_item_big_price(api_client, unique_seller_id):
    """Проверяем, что обычная цена принимается."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Дорого",
        price=999999,
    )
    assert response.status_code == 200
    item_id = api_client.extract_id(response)
    assert item_id is not None
    item_data = api_client.get_item_by_id(item_id)
    assert item_data.status_code == 200
    assert item_data.json()[0]["price"] == 999999


@allure.title("TC-004: Создание объявления со статистикой 1,1,1")
@pytest.mark.positive
def test_create_item_min_statistics(api_client, unique_seller_id):
    """Проверяем, что минимальная ненулевая статистика принимается."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Мин статистика",
        price=100,
        statistics={"likes": 1, "viewCount": 1, "contacts": 1},
    )
    assert response.status_code == 200
    item_id = api_client.extract_id(response)
    assert item_id is not None
    item_data = api_client.get_item_by_id(item_id)
    assert item_data.status_code == 200
    data = item_data.json()[0]
    assert data["statistics"]["likes"] == 1
    assert data["statistics"]["viewCount"] == 1
    assert data["statistics"]["contacts"] == 1


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
    item_id = api_client.extract_id(response)
    assert item_id is not None
    item_data = api_client.get_item_by_id(item_id)
    assert item_data.status_code == 200
    data = item_data.json()[0]
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
        item_id = api_client.extract_id(response)
        assert item_id is not None

    result = api_client.get_items_by_seller(unique_seller_id)
    assert result.status_code == 200
    items = result.json()
    assert len(items) >= 3


@allure.title("TC-007: Разные продавцы получают разные ID")
@pytest.mark.positive
def test_unique_ids_for_different_sellers(api_client):
    """Проверяем, что у разных продавцов разные ID объявлений."""
    response1 = api_client.create_test_item(seller_id=222222, name="Продавец 1", price=100)
    response2 = api_client.create_test_item(seller_id=333333, name="Продавец 2", price=200)
    assert response1.status_code == 200
    assert response2.status_code == 200
    id1 = api_client.extract_id(response1)
    id2 = api_client.extract_id(response2)
    assert id1 is not None
    assert id2 is not None
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
    item_id = api_client.extract_id(response)
    assert item_id is not None
    item_data = api_client.get_item_by_id(item_id)
    assert item_data.status_code == 200
    assert item_data.json()[0]["name"] == "Персидский котёнок"
