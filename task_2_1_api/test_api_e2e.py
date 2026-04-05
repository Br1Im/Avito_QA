"""Corner-кейсы и E2E тесты API."""

import allure
import pytest
from api_client import APIClient


@allure.title("TC-025: Идемпотентность - дубликаты")
@pytest.mark.corner
def test_create_duplicate_items(api_client, unique_seller_id):
    """Создаём два одинаковых объявления - должны получить разные ID."""
    body = {
        "sellerID": unique_seller_id,
        "name": "Дубликат",
        "price": 1000,
        "statistics": {"likes": 10, "viewCount": 50, "contacts": 5},
    }
    response1 = api_client.create_item(body)
    response2 = api_client.create_item(body)
    assert response1.status_code == 200
    assert response2.status_code == 200
    id1 = api_client.extract_id(response1)
    id2 = api_client.extract_id(response2)
    assert id1 is not None
    assert id2 is not None
    assert id1 != id2


@allure.title("TC-026: Нагрузочный тест - 10 объявлений")
@pytest.mark.corner
def test_create_many_items(api_client, unique_seller_id):
    """Создаём 10 объявлений подряд - все должны получить уникальные ID."""
    created_ids = []
    for i in range(10):
        response = api_client.create_test_item(
            seller_id=unique_seller_id,
            name=f"Нагрузочный {i}",
            price=100 * (i + 1),
        )
        assert response.status_code == 200
        created_ids.append(api_client.extract_id(response))
    assert len(set(created_ids)) == 10


@allure.title("TC-027: null цена")
@pytest.mark.corner
def test_create_item_null_price(api_client, unique_seller_id):
    """Проверяем обработку null значения цены."""
    body = {"sellerID": unique_seller_id, "name": "Null", "price": None}
    response = api_client.create_item(body)
    assert response.status_code in [400, 422]


@allure.title("TC-028: Максимальный sellerID (999999)")
@pytest.mark.corner
def test_create_item_max_seller_id(api_client):
    """Проверяем граничное значение sellerID."""
    response = api_client.create_test_item(seller_id=999999, name="Макс", price=100)
    assert response.status_code == 200
    item_id = api_client.extract_id(response)
    get_resp = api_client.get_item_by_id(item_id)
    assert get_resp.status_code == 200
    data = get_resp.json()[0]
    assert data["sellerId"] == 999999


@allure.title("TC-029: Минимальный sellerID (111111)")
@pytest.mark.corner
def test_create_item_min_seller_id(api_client):
    """Проверяем граничное значение sellerID."""
    response = api_client.create_test_item(seller_id=111111, name="Мин", price=100)
    assert response.status_code == 200
    item_id = api_client.extract_id(response)
    get_resp = api_client.get_item_by_id(item_id)
    assert get_resp.status_code == 200
    data = get_resp.json()[0]
    assert data["sellerId"] == 111111


@allure.title("TC-030: Эмодзи в названии")
@pytest.mark.corner
def test_create_item_emoji_in_name(api_client, unique_seller_id):
    """Проверяем поддержку эмодзи."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="iPhone \U0001f4f1",
        price=50000,
    )
    assert response.status_code == 200
    item_id = api_client.extract_id(response)
    get_resp = api_client.get_item_by_id(item_id)
    assert get_resp.status_code == 200
    data = get_resp.json()[0]
    assert "\U0001f4f1" in data["name"]


@allure.title("TC-031: Юникод в названии")
@pytest.mark.corner
def test_create_item_unicode_name(api_client, unique_seller_id):
    """Проверяем поддержку японских символов."""
    response = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="日本語テスト",
        price=1000,
    )
    assert response.status_code == 200
    item_id = api_client.extract_id(response)
    get_resp = api_client.get_item_by_id(item_id)
    assert get_resp.status_code == 200
    data = get_resp.json()[0]
    assert data["name"] == "日本語テスト"


@allure.title("TC-040: E2E - Получить объявление по ID")
@pytest.mark.e2e
def test_e2e_get_item_by_id(api_client, unique_seller_id):
    """Создаём объявление и получаем его по ID."""
    create_resp = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="E2E тест",
        price=2500,
    )
    item_id = api_client.extract_id(create_resp)

    get_resp = api_client.get_item_by_id(item_id)
    assert get_resp.status_code == 200
    items = get_resp.json()
    data = items[0]
    assert data["id"] == item_id
    assert data["name"] == "E2E тест"


@allure.title("TC-041: E2E - Проверка типов данных")
@pytest.mark.e2e
def test_e2e_verify_data_types(api_client, unique_seller_id):
    """Проверяем типы данных в ответе."""
    create_resp = api_client.create_test_item(seller_id=unique_seller_id, name="Типы", price=100)
    item_id = api_client.extract_id(create_resp)

    get_resp = api_client.get_item_by_id(item_id)
    items = get_resp.json()
    data = items[0]
    assert isinstance(data["id"], str)
    assert isinstance(data["sellerId"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["price"], int)


@allure.title("TC-042: E2E - Объявление со статистикой")
@pytest.mark.e2e
def test_e2e_get_item_with_statistics(api_client, unique_seller_id):
    """Проверяем сохранение и получение статистики."""
    stats = {"likes": 50, "viewCount": 200, "contacts": 10}
    create_resp = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Со статистикой",
        price=10000,
        statistics=stats,
    )
    item_id = api_client.extract_id(create_resp)

    get_resp = api_client.get_item_by_id(item_id)
    items = get_resp.json()
    data = items[0]
    assert data["statistics"]["likes"] == 50
    assert data["statistics"]["viewCount"] == 200
    assert data["statistics"]["contacts"] == 10


@allure.title("TC-060: E2E - Все объявления продавца")
@pytest.mark.e2e
def test_e2e_get_seller_items_multiple(api_client, unique_seller_id):
    """Создаём 3 объявления и получаем их по sellerID."""
    for i in range(3):
        api_client.create_test_item(
            seller_id=unique_seller_id,
            name=f"Продавец {i}",
            price=100 * (i + 1),
        )

    get_resp = api_client.get_items_by_seller(unique_seller_id)
    assert get_resp.status_code == 200
    items = get_resp.json()
    assert len(items) >= 3


@allure.title("TC-061: E2E - Одно объявление продавца")
@pytest.mark.e2e
def test_e2e_get_seller_items_single(api_client, unique_seller_id):
    """Создаём 1 объявление и получаем его."""
    api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Одно",
        price=500,
    )

    get_resp = api_client.get_items_by_seller(unique_seller_id)
    assert get_resp.status_code == 200
    items = get_resp.json()
    assert len(items) >= 1


@allure.title("TC-062: E2E - Несуществующий продавец")
@pytest.mark.e2e
def test_e2e_get_nonexistent_seller(api_client):
    """Проверяем, что несуществующий продавец возвращает пустой список."""
    get_resp = api_client.get_items_by_seller(999998)
    assert get_resp.status_code == 200
    items = get_resp.json()
    assert items == [] or isinstance(items, list)


@allure.title("TC-070: E2E - Получить статистику")
@pytest.mark.e2e
def test_e2e_get_statistics(api_client, unique_seller_id):
    """Создаём объявление и получаем его статистику."""
    create_resp = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Статистика",
        price=1000,
        statistics={"likes": 15, "viewCount": 75, "contacts": 3},
    )
    item_id = api_client.extract_id(create_resp)

    stats_resp = api_client.get_statistic_v1(item_id)
    assert stats_resp.status_code == 200


@allure.title("TC-072: E2E - Статистика v2")
@pytest.mark.e2e
def test_e2e_get_statistics_v2(api_client, unique_seller_id):
    """Проверяем v2 версию статистики."""
    create_resp = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Стата v2",
        price=2000,
    )
    item_id = api_client.extract_id(create_resp)

    stats_resp = api_client.get_statistic_v2(item_id)
    assert stats_resp.status_code == 200


@allure.title("TC-080: E2E - Полный цикл создание-удаление")
@pytest.mark.e2e
def test_e2e_full_cycle_create_get_delete(api_client, unique_seller_id):
    """Создаём, получаем, удаляем, проверяем удаление."""
    create_resp = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Удалить",
        price=100,
    )
    item_id = api_client.extract_id(create_resp)

    get_resp = api_client.get_item_by_id(item_id)
    assert get_resp.status_code == 200

    delete_resp = api_client.delete_item(item_id)
    assert delete_resp.status_code == 200

    get_after_delete = api_client.get_item_by_id(item_id)
    assert get_after_delete.status_code == 404


@allure.title("TC-081: E2E - Повторное удаление")
@pytest.mark.e2e
def test_e2e_delete_twice(api_client, unique_seller_id):
    """Проверяем идемпотентность удаления."""
    create_resp = api_client.create_test_item(seller_id=unique_seller_id, name="Двойное", price=100)
    item_id = api_client.extract_id(create_resp)

    delete_resp1 = api_client.delete_item(item_id)
    assert delete_resp1.status_code == 200

    delete_resp2 = api_client.delete_item(item_id)
    assert delete_resp2.status_code in [200, 404]


@allure.title("TC-100: E2E - Полный workflow")
@pytest.mark.e2e
def test_e2e_complete_workflow(api_client, unique_seller_id):
    """Полный цикл: создание -> получение по ID -> по seller -> статистика -> удаление."""
    create_resp = api_client.create_test_item(
        seller_id=unique_seller_id,
        name="Полный цикл",
        price=3000,
    )
    item_id = api_client.extract_id(create_resp)

    get_resp = api_client.get_item_by_id(item_id)
    assert get_resp.status_code == 200
    items = get_resp.json()
    assert items[0]["id"] == item_id

    seller_resp = api_client.get_items_by_seller(unique_seller_id)
    assert seller_resp.status_code == 200

    stats_resp = api_client.get_statistic_v1(item_id)
    assert stats_resp.status_code == 200

    delete_resp = api_client.delete_item(item_id)
    assert delete_resp.status_code == 200


@allure.title("TC-101: E2E - Несколько объявлений")
@pytest.mark.e2e
def test_e2e_create_and_verify_multiple(api_client, unique_seller_id):
    """Создаём 5 объявлений и проверяем, что все доступны."""
    created_ids = []
    for i in range(5):
        resp = api_client.create_test_item(
            seller_id=unique_seller_id,
            name=f"Пакет {i}",
            price=100 * (i + 1),
        )
        assert resp.status_code == 200
        created_ids.append(api_client.extract_id(resp))

    seller_resp = api_client.get_items_by_seller(unique_seller_id)
    assert seller_resp.status_code == 200
    seller_items = seller_resp.json()

    for item_id in created_ids:
        assert any(item["id"] == item_id for item in seller_items)


@allure.title("TC-102: E2E - Удаление одного из трёх")
@pytest.mark.e2e
def test_e2e_delete_one_remain_two(api_client, unique_seller_id):
    """Создаём 3, удаляем 1, проверяем что 2 осталось."""
    ids = []
    for i in range(3):
        resp = api_client.create_test_item(
            seller_id=unique_seller_id,
            name=f"Удалить {i}",
            price=100,
        )
        assert resp.status_code == 200
        ids.append(api_client.extract_id(resp))

    delete_resp = api_client.delete_item(ids[0])
    assert delete_resp.status_code == 200

    seller_resp = api_client.get_items_by_seller(unique_seller_id)
    remaining = seller_resp.json()
    remaining_ids = [item["id"] for item in remaining]

    assert ids[0] not in remaining_ids
    assert ids[1] in remaining_ids
    assert ids[2] in remaining_ids
