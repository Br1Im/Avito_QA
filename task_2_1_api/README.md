# API тесты (Задание 2.1)

## Структура

- `api_client.py` - обёртка над requests для работы с API
- `conftest.py` - фикстуры pytest (api_client, unique_seller_id, created_item)
- `test_api_positive.py` - позитивные тест-кейсы
- `test_api_negative.py` - негативные тест-кейсы
- `test_api_e2e.py` - E2E и корнер-кейсы
- `test_api_nonfunctional.py` - производительность, CORS

## Запуск тестов

Из корня проекта:
```bash
pytest task_2_1_api/ -v
```

Из этой папки:
```bash
pytest . -v
```

С маркерами:
```bash
pytest task_2_1_api/ -m positive -v
pytest task_2_1_api/ -m negative -v
pytest task_2_1_api/ -m e2e -v
pytest task_2_1_api/ -m corner -v
pytest task_2_1_api/ -m nonfunctional -v
```

## Allure отчёты

```bash
pytest task_2_1_api/ --alluredir=task_2_1_api/allure-results
allure serve task_2_1_api/allure-results
```

## Линтер и форматтер

Проект использует ruff. Конфигурация в `pyproject.toml` в корне проекта.

Проверка кода:
```bash
ruff check task_2_1_api/
```

Автоформатирование:
```bash
ruff format task_2_1_api/
```

## Зависимости

```bash
pip install -r requirements.txt
```

Тесты требуют:
- pytest
- requests
- allure-pytest
- ruff (для линтера)
