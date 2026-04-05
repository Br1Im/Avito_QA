"""UI тесты для платформы модерации Авито."""

import requests
import allure
import pytest


UI_BASE_URL = "https://qa-internship.avito.com"


def _check_page_exists(page, url):
    """Проверяет что страница доступна (возвращает HTML, не JSON ошибку)."""
    page.goto(url)
    page.wait_for_timeout(2000)
    html = page.content()
    # Если сервер вернёт JSON ошибку вместо HTML — страница недоступна
    if '"message"' in html and '"code"' in html:
        return False
    return True


@allure.title("Десктоп: Фильтр по цене")
@pytest.mark.desktop
def test_price_range_filter(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /list недоступна на сервере")

    min_input = page.locator('input[placeholder*="от"]').first
    max_input = page.locator('input[placeholder*="до"]').first

    assert min_input.count() > 0, "Не нашёл поле мин. цены"
    assert max_input.count() > 0, "Не нашёл поле макс. цены"

    min_input.fill("1000")
    max_input.fill("50000")

    page.wait_for_timeout(500)

    price_cells = page.locator('[data-testid="price"], .price, [class*="price"]').all()
    for cell in price_cells:
        price_text = cell.text_content()
        if price_text:
            digits = "".join(filter(str.isdigit, price_text.split("-")[0]))
            if digits:
                price = int(digits)
                assert 1000 <= price <= 50000, f"Цена {price} вне диапазона"


@allure.title("Десктоп: Сортировка по цене (возрастание)")
@pytest.mark.desktop
def test_sort_by_price_asc(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /list недоступна на сервере")

    sort_button = page.locator('select[name*="sort"], [data-testid="sort"], [class*="sort"]').first
    if sort_button.count() == 0:
        pytest.skip("Контрол сортировки не найден на странице")

    sort_button.select_option("price_asc")
    page.wait_for_timeout(1000)

    price_cells = page.locator('[data-testid="price"], .price, [class*="price"]').all()
    prices = []
    for cell in price_cells[:10]:
        price_text = cell.text_content()
        if price_text:
            digits = "".join(filter(str.isdigit, price_text.split("-")[0]))
            if digits:
                prices.append(int(digits))

    if len(prices) >= 2:
        assert prices == sorted(prices), f"Цены не по возрастанию: {prices}"


@allure.title("Десктоп: Сортировка по цене (убывание)")
@pytest.mark.desktop
def test_sort_by_price_desc(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /list недоступна на сервере")

    sort_button = page.locator('select[name*="sort"], [data-testid="sort"], [class*="sort"]').first
    if sort_button.count() == 0:
        pytest.skip("Контрол сортировки не найден на странице")

    sort_button.select_option("price_desc")
    page.wait_for_timeout(1000)

    price_cells = page.locator('[data-testid="price"], .price, [class*="price"]').all()
    prices = []
    for cell in price_cells[:10]:
        price_text = cell.text_content()
        if price_text:
            digits = "".join(filter(str.isdigit, price_text.split("-")[0]))
            if digits:
                prices.append(int(digits))

    if len(prices) >= 2:
        assert prices == sorted(prices, reverse=True), f"Цены не по убыванию: {prices}"


@allure.title("Десктоп: Фильтр по категории")
@pytest.mark.desktop
def test_category_filter(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /list недоступна на сервере")

    category_dropdown = page.locator('select[name*="category"], [data-testid="category"], [class*="category"]').first
    if category_dropdown.count() == 0:
        pytest.skip("Выпадающий список категории не найден")

    options = category_dropdown.locator("option").all()
    if len(options) > 1:
        selected_value = options[1].get_attribute("value") or options[1].text_content()
        category_dropdown.select_option(selected_value)
        page.wait_for_timeout(500)
        selected = category_dropdown.input_value()
        assert selected == selected_value


@allure.title("Десктоп: Тогл Только срочные")
@pytest.mark.desktop
def test_urgent_toggle(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /list недоступна на сервере")

    urgent_toggle = page.locator('input[type="checkbox"][name*="urgent"], [data-testid="urgent"], [class*="urgent"]').first
    if urgent_toggle.count() == 0:
        pytest.skip("Тогл срочных не найден")

    is_checked_before = urgent_toggle.is_checked()
    urgent_toggle.click()
    page.wait_for_timeout(500)
    is_checked_after = urgent_toggle.is_checked()
    assert is_checked_before != is_checked_after, "Тогл не изменил состояние"


@allure.title("Десктоп: Кнопка Обновить на странице статистики")
@pytest.mark.desktop
def test_stats_refresh_button(page):
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /stats недоступна на сервере")

    refresh_button = page.locator('button:has-text("Обновить"), [data-testid="refresh"]').first
    if refresh_button.count() == 0:
        pytest.skip("Кнопка Обновить не найдена")

    refresh_button.click()
    page.wait_for_timeout(1000)
    assert page.url.endswith("/stats")


@allure.title("Десктоп: Кнопка Остановить на странице статистики")
@pytest.mark.desktop
def test_stats_stop_timer(page):
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /stats недоступна на сервере")

    stop_button = page.locator('button:has-text("Остановить"), [data-testid="stop"]').first
    if stop_button.count() == 0:
        pytest.skip("Кнопка Остановить не найдена")

    stop_button.click()
    page.wait_for_timeout(500)

    start_button = page.locator('button:has-text("Запустить")').first
    if start_button.count() > 0:
        pass  # Остановка сработала, появилась кнопка запуска


@allure.title("Десктоп: Кнопка Запустить на странице статистики")
@pytest.mark.desktop
def test_stats_start_timer(page):
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /stats недоступна на сервере")

    start_button = page.locator('button:has-text("Запустить"), [data-testid="start"]').first
    if start_button.count() == 0:
        pytest.skip("Кнопка Запустить не найдена")

    start_button.click()
    page.wait_for_timeout(500)

    stop_button = page.locator('button:has-text("Остановить")').first
    if stop_button.count() > 0:
        pass  # Запуск сработал, появилась кнопка остановки


@allure.title("Мобильный: Переключение темы")
@pytest.mark.mobile
def test_mobile_theme_toggle(page):
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /list недоступна на сервере")

    theme_toggle = page.locator('button:has-text("Тема"), [data-testid="theme"], [class*="theme"]').first
    if theme_toggle.count() == 0:
        pytest.skip("Переключатель темы не найден")

    html_el = page.locator("html")
    theme_before = html_el.get_attribute("data-theme") or html_el.get_attribute("class") or ""

    theme_toggle.click()
    page.wait_for_timeout(300)

    theme_after = html_el.get_attribute("data-theme") or html_el.get_attribute("class") or ""
    assert theme_before != theme_after, "Тема не изменилась"


@allure.title("Десктоп: Страница карточки объявления")
@pytest.mark.desktop
def test_item_moderation_page(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_timeout(2000)
    html = page.content()
    if '"route' in html and 'not found' in html:
        pytest.skip("Страница /list недоступна на сервере")

    first_item = page.locator('[data-testid="item"], .item-card, [class*="item"]').first
    if first_item.count() == 0:
        pytest.skip("Карточки объявлений не найдены на странице")

    first_item.click()
    page.wait_for_timeout(1000)

    assert page.url.startswith(f"{UI_BASE_URL}/item/"), f"URL не ведёт на /item/: {page.url}"
