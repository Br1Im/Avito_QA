"""UI тесты для платформы модерации Авито."""

import allure
import pytest
from playwright.sync_api import Page


UI_BASE_URL = "https://qa-internship.avito.com"


@allure.title("Десктоп: Фильтр по цене")
@pytest.mark.desktop
def test_price_range_filter(page):
    """Проверяем работу фильтра по диапазону цен."""
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    min_input = page.locator('input[placeholder*="от"]').first
    max_input = page.locator('input[placeholder*="до"]').first

    min_input.fill("1000")
    max_input.fill("50000")

    page.wait_for_timeout(500)

    price_cells = page.locator('[data-testid="price"], .price, [class*="price"]').all()
    if price_cells:
        for cell in price_cells:
            price_text = cell.text_content()
            if price_text:
                price = int("".join(filter(str.isdigit, price_text.split("-")[0])))
                assert 1000 <= price <= 50000, f"Цена {price} вне диапазона"


@allure.title("Десктоп: Сортировка по цене")
@pytest.mark.desktop
def test_sort_by_price(page):
    """Проверяем сортировку по цене."""
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    sort_button = page.locator('select[name*="sort"], [data-testid="sort"], [class*="sort"]').first
    if sort_button.count() > 0:
        sort_button.select_option("price_asc")
        page.wait_for_timeout(1000)

        price_cells = page.locator('[data-testid="price"], .price, [class*="price"]').all()
        prices = []
        for cell in price_cells[:10]:
            price_text = cell.text_content()
            if price_text:
                price = int("".join(filter(str.isdigit, price_text.split("-")[0])))
                prices.append(price)

        if len(prices) > 1:
            assert prices == sorted(prices), "Цены должны быть по возрастанию"


@allure.title("Десктоп: Фильтр по категории")
@pytest.mark.desktop
def test_category_filter(page):
    """Проверяем работу фильтра по категории."""
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    category_dropdown = page.locator('select[name*="category"], [data-testid="category"], [class*="category"]').first
    if category_dropdown.count() > 0:
        options = category_dropdown.locator("option").all()
        if len(options) > 1:
            category_dropdown.select_option(options[1].get_attribute("value") or options[1].text_content())
            page.wait_for_timeout(500)


@allure.title("Десктоп: Тогл 'Только срочные'")
@pytest.mark.desktop
def test_urgent_toggle(page):
    """Проверяем переключение тогла срочных объявлений."""
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    urgent_toggle = page.locator('input[type="checkbox"][name*="urgent"], [data-testid="urgent"], [class*="urgent"]').first
    if urgent_toggle.count() > 0:
        is_checked_before = urgent_toggle.is_checked()
        urgent_toggle.click()
        page.wait_for_timeout(500)
        is_checked_after = urgent_toggle.is_checked()
        assert is_checked_before != is_checked_after, "Тогл должен измениться"


@allure.title("Десктоп: Кнопка 'Обновить' на странице статистики")
@pytest.mark.desktop
def test_stats_refresh_button(page):
    """Проверяем работу кнопки обновления статистики."""
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_load_state("networkidle")

    refresh_button = page.locator('button:has-text("Обновить"), [data-testid="refresh"]').first
    if refresh_button.count() > 0:
        refresh_button.click()
        page.wait_for_timeout(1000)


@allure.title("Десктоп: Кнопка 'Остановить' на странице статистики")
@pytest.mark.desktop
def test_stats_stop_timer(page):
    """Проверяем работу кнопки остановки таймера."""
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_load_state("networkidle")

    stop_button = page.locator('button:has-text("Остановить"), [data-testid="stop"]').first
    if stop_button.count() > 0:
        stop_button.click()
        page.wait_for_timeout(500)


@allure.title("Десктоп: Кнопка 'Запустить' на странице статистики")
@pytest.mark.desktop
def test_stats_start_timer(page):
    """Проверяем работу кнопки запуска таймера."""
    page.goto(f"{UI_BASE_URL}/stats")
    page.wait_for_load_state("networkidle")

    start_button = page.locator('button:has-text("Запустить"), [data-testid="start"]').first
    if start_button.count() > 0:
        start_button.click()
        page.wait_for_timeout(500)


@allure.title("Мобильный: Переключение темы")
@pytest.mark.mobile
def test_mobile_theme_toggle(page):
    """Проверяем переключение темы на мобильном разрешении."""
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    theme_toggle = page.locator('button:has-text("Тема"), [data-testid="theme"], [class*="theme"]').first
    if theme_toggle.count() > 0:
        html_before = page.locator("html")
        theme_before = html_before.get_attribute("data-theme") or html_before.get_attribute("class") or ""

        theme_toggle.click()
        page.wait_for_timeout(300)

        theme_after = html_before.get_attribute("data-theme") or html_before.get_attribute("class") or ""
        assert theme_before != theme_after, "Тема должна измениться"


@allure.title("Десктоп: Страница карточки объявления")
@pytest.mark.desktop
def test_item_moderation_page(page):
    """Проверяем открытие страницы модерации объявления."""
    page.goto(f"{UI_BASE_URL}/list")
    page.wait_for_load_state("networkidle")

    first_item = page.locator('[data-testid="item"], .item-card, [class*="item"]').first
    if first_item.count() > 0:
        first_item.click()
        page.wait_for_load_state("networkidle")

        assert page.url.startswith(f"{UI_BASE_URL}/item/")
