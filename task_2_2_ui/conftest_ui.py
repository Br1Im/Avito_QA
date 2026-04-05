"""Конфигурация Playwright для UI тестов."""

import pytest
from playwright.sync_api import sync_playwright


def pytest_configure(config):
    config.addinivalue_line("markers", "desktop: десктопные тесты")
    config.addinivalue_line("markers", "mobile: мобильные тесты")


@pytest.fixture(scope="session")
def browser():
    """Запускает браузер для тестов."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """Создаёт новую страницу для каждого теста."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
