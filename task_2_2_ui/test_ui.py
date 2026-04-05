"""UI тесты для платформы модерации Авито."""

import allure
import pytest
from playwright.sync_api import Page


UI_BASE_URL = "https://qa-internship.avito.com"


@allure.title("Десктоп: Фильтр по цене")
@pytest.mark.desktop
def test_price_range_filter(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    min_input = page.locator('input[placeholder*="от"]').first
    max_input = page.locator('input[placeholder*="до"]').first

    min_input.fill("1000")
    max_input.fill("50000")

    page.wait_for_timeout(500)

    price_cells = page.locator('[data-testid="price"], .price, [class*="price"]').all()
    for cell in price_cells:
        price_text = cell.text_content()
        if price_text:
            price = int("".join(filter(str.isdigit, price_text.split("-")[0])))
            assert 1000 <= price <= 50000, f"Цена {price} вне диапазона"


@allure.title("Десктоп: Сортировка по цене (возрастание)")
@pytest.mark.desktop
def test_sort_by_price_asc(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    sort_button = page.locator('select[name*="sort"], [data-testid="sort"], [class*="sort"]').first
    assert sort_button.count() > 0, "Не нашёл сортировку"

    sort_button.select_option("price_asc")
    page.wait_for_timeout(1000)

    price_cells = page.locator('[data-testid="price"], .price, [class*="price"]').all()
    prices = []
    for cell in price_cells[:10]:
        price_text = cell.text_content()
        if price_text:
            price = int("".join(filter(str.isdigit, price_text.split("-")[0])))
            prices.append(price)

    assert len(prices) >= 2, "Мало объявлений для проверки сортировки"
    assert prices == sorted(prices), f"Цены не по возрастанию: {prices}"


@allure.title("Десктоп: Сортировка по цене (убывание)")
@pytest.mark.desktop
def test_sort_by_price_desc(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    sort_button = page.locator('select[name*="sort"], [data-testid="sort"], [class*="sort"]').first
    assert sort_button.count() > 0, "Не нашёл сортировку"

    sort_button.select_option("price_desc")
    page.wait_for_timeout(1000)

    price_cells = page.locator('[data-testid="price"], .price, [class*="price"]').all()
    prices = []
    for cell in price_cells[:10]:
        price_text = cell.text_content()
        if price_text:
            price = int("".join(filter(str.isdigit, price_text.split("-")[0])))
            prices.append(price)

    assert len(prices) >= 2, "Мало объявлений для проверки сортировки"
    assert prices == sorted(prices, reverse=True), f"Цены не по убыванию: {prices}"


@allure.title("Десктоп: Фильтр по категории")
@pytest.mark.desktop
def test_category_filter(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    category_dropdown = page.locator('select[name*="category"], [data-testid="category"], [class*="category"]').first
    assert category_dropdown.count() > 0, "Не нашёл дропдаун категории"

    options = category_dropdown.locator("option").all()
    assert len(options) > 1, "В категории меньше 2 опций"

    selected_value = options[1].get_attribute("value") or options[1].text_content()
    category_dropdown.select_option(selected_value)
    page.wait_for_timeout(500)

    selected = category_dropdown.input_value()
    assert selected == selected_value, f"Выбрано '{selected}', ожидалось '{selected_value}'"


@allure.title("Десктоп: Тогл 'Только срочные'")
@pytest.mark.desktop
def test_urgent_toggle(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    urgent_toggle = page.locator('input[type="checkbox"][name*="urgent"], [data-testid="urgent"], [class*="urgent"]').first
    assert urgent_toggle.count() > 0, "Не нашёл тогл 'Только срочные'"

    is_checked_before = urgent_toggle.is_checked()
    urgent_toggle.click()
    page.wait_for_timeout(500)
    is_checked_after = urgent_toggle.is_checked()
    assert is_checked_before != is_checked_after, "Тогл не изменил состояние"


@allure.title("Десктоп: Кнопка 'Обновить' на странице статистики")
@pytest.mark.desktop
def test_stats_refresh_button(page):
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_load_state("networkidle")

    refresh_button = page.locator('button:has-text("Обновить"), [data-testid="refresh"]').first
    assert refresh_button.count() > 0, "Не нашёл кнопку 'Обновить'"

    refresh_button.click()
    page.wait_for_timeout(1000)

    assert page.url.endswith("/stats"), "После обновления остались на /stats"


@allure.title("Десктоп: Кнопка 'Остановить' на странице статистики")
@pytest.mark.desktop
def test_stats_stop_timer(page):
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_load_state("networkidle")

    stop_button = page.locator('button:has-text("Остановить"), [data-testid="stop"]').first
    assert stop_button.count() > 0, "Не нашёл кнопку 'Остановить'"

    stop_button.click()
    page.wait_for_timeout(500)

    start_button = page.locator('button:has-text("Запустить")').first
    assert start_button.count() > 0, "После остановки не появилась кнопка 'Запустить'"


@allure.title("Десктоп: Кнопка 'Запустить' на странице статистики")
@pytest.mark.desktop
def test_stats_start_timer(page):
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_load_state("networkidle")

    start_button = page.locator('button:has-text("Запустить"), [data-testid="start"]').first
    assert start_button.count() > 0, "Не нашёл кнопку 'Запустить'"

    start_button.click()
    page.wait_for_timeout(500)

    stop_button = page.locator('button:has-text("Остановить")').first
    assert stop_button.count() > 0, "После запуска не появилась кнопка 'Остановить'"


@allure.title("Мобильный: Переключение темы")
@pytest.mark.mobile
def test_mobile_theme_toggle(page):
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    theme_toggle = page.locator('button:has-text("Тема"), [data-testid="theme"], [class*="theme"]').first
    assert theme_toggle.count() > 0, "Не нашёл переключатель темы"

    html = page.locator("html")
    theme_before = html.get_attribute("data-theme") or html.get_attribute("class") or ""

    theme_toggle.click()
    page.wait_for_timeout(300)

    theme_after = html.get_attribute("data-theme") or html.get_attribute("class") or ""
    assert theme_before != theme_after, "Тема не изменилась"


@allure.title("Десктоп: Страница карточки объявления")
@pytest.mark.desktop
def test_item_moderation_page(page):
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    first_item = page.locator('[data-testid="item"], .item-card, [class*="item"]').first
    assert first_item.count() > 0, "Не нашёл карточки объявлений"

    first_item.click()
    page.wait_for_load_state("networkidle")

    assert page.url.startswith(f"{UI_BASE_URL}/item/"), f"URL не ведёт на /item/: {page.url}"
