# Avito Internship — Задание 2

Набор тестов для API и UI, всё что нужно для проверки.

## Что внутри

- **task_2_1_api/** — тесты API (позитивные, негативные, e2e, плюс нефункциональные)
- **task_2_2_ui/** — UI-тесты через Playwright
- **TESTCASES.md** — все тест-кейсы
- **BUGS.md** — найденные баги

## Как запустить

Сначала зависимости:

```bash
pip install -r requirements.txt
playwright install chromium
```

### API тесты

```bash
pytest task_2_1_api/ -v
```

### UI тесты

```bash
pytest task_2_2_ui/ -v
```

## Allure

Можно посмотреть отчёты:

```bash
# API
pytest task_2_1_api/ --alluredir=task_2_1_api/allure-results
allure serve task_2_1_api/allure-results

# UI
pytest task_2_2_ui/ --alluredir=task_2_2_ui/allure-results
allure serve task_2_2_ui/allure-results
```

## Линтер

Перед отправкой проверял через ruff:

```bash
ruff check task_2_1_api/
```
