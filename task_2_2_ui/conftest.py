"""Фикстуры для UI тестов."""

import pytest


BASE_URL = "https://cerulean-praline-8e5aa6.netlify.app"


@pytest.fixture
def ui_mobile_page(browser):
    """Мобильная страница - отдельный контекст."""
    context = browser.new_context(viewport={"width": 375, "height": 667})
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def ui_stats_page(page):
    """Страница статистики - переход по клику."""
    page.goto(BASE_URL)
    page.wait_for_timeout(2000)
    page.locator('a:has-text("Статистика")').click()
    page.wait_for_timeout(2000)
    return page
