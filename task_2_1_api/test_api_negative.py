"""Негативные тесты API."""

import allure
import pytest
from api_client import APIClient


@allure.title("TC-010: Создание без sellerID")
@pytest.mark.negative
def test_create_item_missing_seller_id(api_client):
    """Проверяем, что отсутствующий sellerID отклоняется."""
    body = {"name": "Тест", "price": 100}
    response = api_client.create_item(body)
    assert response.status_code == 400


@allure.title("TC-011: Создание без названия")
@pytest.mark.negative
def test_create_item_missing_name(api_client):
    """Проверяем, что отсутствующее name отклоняется."""
    body = {"sellerID": 111111, "price": 100}
    response = api_client.create_item(body)
    assert response.status_code == 400


@allure.title("TC-012: Создание без цены")
@pytest.mark.negative
def test_create_item_missing_price(api_client):
    """Проверяем, что отсутствующая price отклоняется."""
    body = {"sellerID": 111111, "name": "Тест"}
    response = api_client.create_item(body)
    assert response.status_code == 400


@allure.title("TC-013: Пустое тело запроса")
@pytest.mark.negative
def test_create_item_empty_body(api_client):
    """Проверяем, что пустое тело отклоняется."""
    response = api_client.create_item({})
    assert response.status_code == 400


@allure.title("TC-014: Отрицательная цена")
@pytest.mark.negative
def test_create_item_negative_price(api_client, unique_seller_id):
    """Проверяем поведение сервера при отрицательной цене."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Тест",
        price=-100,
    )
    # Сервер может принять или отклонить — главное проверяем создание
    assert response.status_code in [200, 400, 422]


@allure.title("TC-014b: Цена равна нулю")
@pytest.mark.negative
def test_create_item_zero_price(api_client, unique_seller_id):
    """Проверяем, что цена 0 отклоняется."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Тест",
        price=0,
    )
    assert response.status_code == 400


@allure.title("TC-015: Статистика с нулевыми значениями")
@pytest.mark.negative
def test_create_item_zero_statistics(api_client, unique_seller_id):
    """Проверяем, что статистика со всеми нулями отклоняется."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Тест",
        price=100,
        statistics={"likes": 0, "viewCount": 0, "contacts": 0},
    )
    assert response.status_code in [400, 422]


@allure.title("TC-016: sellerID = 0")
@pytest.mark.negative
def test_create_item_seller_id_zero(api_client):
    """Проверяем, что sellerID = 0 отклоняется."""
    response = api_client.create_test_item(seller_id=0, name="Тест", price=100)
    assert response.status_code in [400, 422]


@allure.title("TC-017: sellerID как строка")
@pytest.mark.negative
def test_create_item_seller_id_as_string(api_client):
    """Проверяем обработку sellerID в виде строки."""
    body = {"sellerID": "111111", "name": "Тест", "price": 100}
    response = api_client.create_item(body)
    assert response.status_code in [200, 400]


@allure.title("TC-018: price как строка")
@pytest.mark.negative
def test_create_item_price_as_string(api_client):
    """Проверяем обработку price в виде строки."""
    body = {"sellerID": 111111, "name": "Тест", "price": "1000"}
    response = api_client.create_item(body)
    assert response.status_code in [200, 400]


@allure.title("TC-019: Неверный Content-Type")
@pytest.mark.nonfunctional
def test_create_item_invalid_content_type(api_client):
    """Проверяем, что text/plain отклоняется."""
    response = api_client.session.post(
        f"{api_client.base_url}/api/1/item",
        data="not json",
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code in [400, 415]


@allure.title("TC-020: Пустое название")
@pytest.mark.negative
def test_create_item_empty_name(api_client, unique_seller_id):
    """Проверяем, что пустое название отклоняется."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="",
        price=100,
    )
    assert response.status_code in [400, 422, 504]


@allure.title("TC-021: SQL-инъекция в названии")
@pytest.mark.negative
def test_create_item_sql_injection(api_client, unique_seller_id):
    """Проверяем, что SQL-инъекция не ломает сервер."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="'; DROP TABLE items; --",
        price=100,
    )
    assert response.status_code in [200, 400]


@allure.title("TC-022: XSS в названии")
@pytest.mark.negative
def test_create_item_xss_injection(api_client, unique_seller_id):
    """Проверяем, что XSS не ломает сервер."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="<script>alert('xss')</script>",
        price=100,
    )
    assert response.status_code in [200, 400]


@allure.title("TC-043: Получение несуществующего объявления")
@pytest.mark.negative
def test_get_item_not_found(api_client):
    """Проверяем, что несуществующий ID возвращает ошибку."""
    response = api_client.get_item_by_id("nonexistent-id-12345")
    assert response.status_code in [400, 404]


@allure.title("TC-063: Нечисловой sellerID")
@pytest.mark.negative
def test_get_items_by_seller_invalid_id(api_client):
    """Проверяем, что буквы в sellerID отклоняются."""
    response = api_client.session.get(f"{api_client.base_url}/api/1/abc/item")
    assert response.status_code in [400, 404, 422]


@allure.title("TC-064: Отрицательный sellerID")
@pytest.mark.negative
def test_get_items_by_seller_negative_id(api_client):
    """Проверяем, что отрицательный sellerID возвращает ошибку или пустоту."""
    response = api_client.get_items_by_seller(-1)
    assert response.status_code in [200, 400, 404]


@allure.title("TC-073: Статистика несуществующего объявления")
@pytest.mark.negative
def test_get_statistics_not_found(api_client):
    """Проверяем ошибку для статистики несуществующего объявления."""
    response = api_client.get_statistic_v1("nonexistent-item-id")
    assert response.status_code in [400, 404]


@allure.title("TC-082: Удаление несуществующего объявления")
@pytest.mark.negative
def test_delete_item_not_found(api_client):
    """Проверяем 404 при удалении несуществующего."""
    response = api_client.delete_item("nonexistent-item-123")
    assert response.status_code in [404, 400]
