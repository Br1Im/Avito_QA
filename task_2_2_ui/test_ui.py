"""UI тесты для платформы модерации объявлений."""

import pytest


BASE_URL = "https://cerulean-praline-8e5aa6.netlify.app"


def _get_prices(page, limit=10):
    """Извлечь цены из карточек через JS (избегаем проблем с кодировкой)."""
    return page.evaluate(
        """(limit) => {
            const elements = document.querySelectorAll('[class*="__price_"]');
            const prices = [];
            elements.forEach((el, i) => {
                if (i >= limit) return;
                const digits = el.textContent.replace(/[^\\d]/g, "");
                if (digits) prices.push(parseInt(digits, 10));
            });
            return prices;
        }""",
        limit,
    )


class TestPriceFilter:
    """TC-01. Фильтр Диапазон цен."""

    @pytest.mark.desktop
    def test_price_filter_valid_range(self, page):
        """1.1 Позитивный сценарий - валидный диапазон."""
        page.goto(BASE_URL + "?minPrice=1000&maxPrice=50000")
        page.wait_for_timeout(3000)

        prices = _get_prices(page)
        assert len(prices) > 0, "Не найдено ни одной карточки с ценой"

        for price in prices:
            assert 1000 <= price <= 50000, f"Цена {price} вне диапазона 1000-50000"

    @pytest.mark.desktop
    def test_price_filter_min_greater_than_max(self, page):
        """1.4 Негативный сценарий - мин больше макс."""
        page.goto(BASE_URL + "?minPrice=5000&maxPrice=1000")
        page.wait_for_timeout(3000)

        price_from = page.locator('[class*="priceRange"] input').first
        price_to = page.locator('[class*="priceRange"] input').nth(1)

        from_val = price_from.input_value() or ""
        to_val = price_to.input_value() or ""

        assert from_val != "5000" or to_val != "1000", "Некорректные параметры применены без валидации"


class TestSortByPrice:
    """TC-02. Сортировка По цене."""

    @pytest.mark.desktop
    def test_sort_price_ascending(self, page):
        """Сортировка по возрастанию."""
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)

        page.locator("select").nth(0).select_option("price")
        page.locator("select").nth(1).select_option("asc")
        page.wait_for_timeout(1000)

        prices = _get_prices(page, 7)
        assert len(prices) >= 2, "Недостаточно карточек для проверки сортировки"
        assert prices == sorted(prices), f"Цены не по возрастанию: {prices}"

    @pytest.mark.desktop
    def test_sort_price_descending(self, page):
        """Сортировка по убыванию."""
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)

        page.locator("select").nth(0).select_option("price")
        page.locator("select").nth(1).select_option("desc")
        page.wait_for_timeout(1000)

        prices = _get_prices(page, 7)
        assert len(prices) >= 2, "Недостаточно карточек для проверки сортировки"
        assert prices == sorted(prices, reverse=True), f"Цены не по убыванию: {prices}"


class TestCategoryFilter:
    """TC-03. Фильтр Категория."""

    @pytest.mark.desktop
    def test_category_filter(self, page):
        """Фильтр по категории."""
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)

        category_select = page.locator("select").nth(2)

        options = category_select.locator("option").all()
        found = False
        for opt in options:
            text = opt.inner_text()
            if "Электроника" in text:
                value = opt.get_attribute("value")
                category_select.select_option(value)
                found = True
                break

        assert found, "Категория Электроника не найдена"
        page.wait_for_timeout(1000)

        categories = page.locator('[class*="__category_"]').all()
        for cat in categories[:10]:
            assert "Электроника" in cat.inner_text(), (
                f"Карточка имеет категорию: {cat.inner_text()}, ожидалась Электроника"
            )

    @pytest.mark.desktop
    def test_category_filter_reset(self, page):
        """Сброс фильтра категории."""
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)

        category_select = page.locator("select").nth(2)

        # Выбрать категорию
        options = category_select.locator("option").all()
        for opt in options:
            text = opt.inner_text()
            if "Электроника" in text:
                category_select.select_option(opt.get_attribute("value"))
                break
        page.wait_for_timeout(1000)

        # Сбросить на "Все категории"
        category_select.select_option("")
        page.wait_for_timeout(1000)

        # Проверка: выбрано "Все категории"
        selected = category_select.input_value()
        assert selected == "", f"Категория не сброшена, текущее значение: {selected}"


class TestUrgentToggle:
    """TC-04. Тоггл Только срочные."""

    @pytest.mark.desktop
    def test_urgent_toggle_on(self, page):
        """Включить тоггл."""
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)

        toggle = page.locator('[class*="urgentToggle"]').first
        toggle.click()
        page.wait_for_timeout(1000)

        checkbox = page.locator('input[type="checkbox"][class*="urgent"]')
        assert checkbox.is_checked(), "Тоггл не включился"

    @pytest.mark.desktop
    def test_urgent_toggle_off(self, page):
        """Выключить тоггл."""
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)

        toggle = page.locator('[class*="urgentToggle"]').first
        toggle.click()
        page.wait_for_timeout(500)
        toggle.click()
        page.wait_for_timeout(500)

        checkbox = page.locator('input[type="checkbox"][class*="urgent"]')
        assert not checkbox.is_checked(), "Тоггл не выключился"


class TestStatsTimer:
    """TC-05. Управление таймером на странице статистики."""

    @pytest.mark.desktop
    def test_refresh_button(self, stats_page):
        """Кнопка Обновить."""
        stats_page.locator('[aria-label="Обновить сейчас"]').click()
        stats_page.wait_for_timeout(1000)

        assert "/stats" in stats_page.url, "Не остались на странице статистики"

    @pytest.mark.desktop
    def test_stop_timer(self, stats_page):
        """Кнопка Остановить."""
        stop_btn = stats_page.locator('[aria-label="Отключить автообновление"]')
        stop_btn.click()
        stats_page.wait_for_timeout(1000)

        start_btn = stats_page.locator('[aria-label="Включить автообновление"]')
        assert start_btn.count() > 0, "Кнопка не изменилась на Включить"

    @pytest.mark.desktop
    def test_start_timer(self, stats_page):
        """Кнопка Запустить."""
        # Сначала останавливаем
        stop_btn = stats_page.locator('[aria-label="Отключить автообновление"]')
        if stop_btn.count() > 0:
            stop_btn.click()
            stats_page.wait_for_timeout(1000)

        # Проверяем что появилась кнопка "Включить"
        start_btn = stats_page.locator('[aria-label="Включить автообновление"]')
        assert start_btn.count() > 0, "Кнопка Включить не появилась"

        # Включаем таймер
        start_btn.click()
        stats_page.wait_for_timeout(3000)

        # Проверяем что кнопка «Включить» исчезла или появилась «Отключить»
        start_still_visible = stats_page.locator('[aria-label="Включить автообновление"]').count() > 0
        stop_visible = stats_page.locator('[aria-label="Отключить автообновление"]').count() > 0

        # После запуска кнопка "Включить" должна исчезнуть или "Отключить" появиться
        # Если ни одно из условий не выполнено — таймер не запустился
        assert stop_visible or not start_still_visible, (
            "Кнопка не изменилась после клика: ни 'Отключить' не появилась, ни 'Включить' не исчезла"
        )


class TestThemeMobile:
    """TC-06. Переключение темы на мобильном."""

    @pytest.mark.mobile
    def test_theme_toggle_mobile(self, mobile_page):
        """Переключение темы."""
        mobile_page.goto(BASE_URL)
        mobile_page.wait_for_timeout(1000)

        html = mobile_page.locator("html")
        theme_before = html.get_attribute("data-theme") or "light"

        theme_btn = mobile_page.locator('[class*="themeToggle"]').first
        theme_btn.click()
        mobile_page.wait_for_timeout(500)

        theme_after = html.get_attribute("data-theme")
        assert theme_before != theme_after, "Тема не изменилась"

    @pytest.mark.mobile
    def test_theme_toggle_back(self, mobile_page):
        """Переключение темы обратно."""
        mobile_page.goto(BASE_URL)
        mobile_page.wait_for_timeout(1000)

        theme_btn = mobile_page.locator('[class*="themeToggle"]').first

        theme_btn.click()
        mobile_page.wait_for_timeout(500)

        theme_btn.click()
        mobile_page.wait_for_timeout(500)

        theme_after = mobile_page.locator("html").get_attribute("data-theme")
        assert theme_after == "light", f"Тема не вернулась в light: {theme_after}"

    @pytest.mark.mobile
    def test_theme_persistence(self, mobile_page):
        """Сохранение темы после перезагрузки."""
        mobile_page.goto(BASE_URL)
        mobile_page.wait_for_timeout(1000)

        theme_btn = mobile_page.locator('[class*="themeToggle"]').first
        theme_btn.click()
        mobile_page.wait_for_timeout(500)

        theme_after_click = mobile_page.locator("html").get_attribute("data-theme")

        mobile_page.reload()
        mobile_page.wait_for_timeout(1000)

        theme_after_reload = mobile_page.locator("html").get_attribute("data-theme")
        assert theme_after_click == theme_after_reload, "Тема не сохранилась после перезагрузки"


@pytest.fixture
def mobile_page(browser):
    """Мобильная страница."""
    context = browser.new_context(viewport={"width": 375, "height": 667})
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def stats_page(page):
    """Страница статистики - переход по клику."""
    page.goto(BASE_URL)
    page.wait_for_timeout(1000)
    page.locator('a:has-text("Статистика")').click()
    page.wait_for_timeout(2000)
    return page


class TestThemeDesktop:
    """TC-18. Переключение темы на десктопе."""

    @pytest.mark.desktop
    def test_theme_toggle_desktop(self, page):
        """Переключение темы на десктопе."""
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)

        html = page.locator("html")
        theme_before = html.get_attribute("data-theme") or "light"

        theme_btn = page.locator('[class*="themeToggle"]').first
        theme_btn.click()
        page.wait_for_timeout(500)

        theme_after = html.get_attribute("data-theme")
        assert theme_before != theme_after, "Тема не изменилась"
