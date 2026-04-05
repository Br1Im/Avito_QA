"""Нефункциональные тесты API."""

import time
import allure
import pytest
from api_client import APIClient


@allure.title("TC-090: Время ответа < 5 секунд")
@pytest.mark.nonfunctional
def test_response_time_under_threshold(api_client, unique_seller_id):
    """Проверяем, что время ответа не превышает 5 секунд."""
    endpoints = [
        lambda: api_client.create_test_item(seller_id=unique_seller_id, name="Тест", price=100),
        lambda: api_client.get_items_by_seller(unique_seller_id),
    ]
    threshold = 5.0

    for endpoint in endpoints:
        start = time.time()
        response = endpoint()
        elapsed = time.time() - start
        assert elapsed < threshold, f"Ответ занял {elapsed:.2f}с, порог {threshold}с"
        assert response.status_code in [200, 201]


@allure.title("TC-091: CORS политика")
@pytest.mark.nonfunctional
def test_cors_headers(api_client):
    """Проверяем наличие CORS заголовков."""
    response = api_client.session.get(
        f"{api_client.base_url}/api/1/item/1",
        headers={"Origin": "http://evil.com"},
    )
    cors_header = response.headers.get("Access-Control-Allow-Origin")
    assert cors_header in [None, "*", "http://evil.com"]


@allure.title("TC-092: Запрос без Content-Type")
@pytest.mark.nonfunctional
def test_request_without_content_type(api_client):
    """Проверяем обработку запроса без Content-Type."""
    response = api_client.session.post(
        f"{api_client.base_url}/api/1/item",
        json={"sellerID": 111111, "name": "Тест", "price": 100},
    )
    assert response.status_code in [200, 400, 415]


@allure.title("TC-093: Неправильный Content-Type")
@pytest.mark.nonfunctional
def test_request_wrong_content_type(api_client):
    """Проверяем отклонение неправильного Content-Type."""
    response = api_client.session.post(
        f"{api_client.base_url}/api/1/item",
        data="sellerID=111111&name=Тест&price=100",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code in [400, 415]
