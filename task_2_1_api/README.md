# Задание 2.1: Тесты API

## Структура

```
task_2_1_api/
├── api_client.py              # API клиент
├── conftest.py               # Фикстуры pytest
├── test_api_positive.py      # Позитивные тесты
├── test_api_negative.py      # Негативные тесты
├── test_api_e2e.py          # E2E тесты
├── test_api_nonfunctional.py # Нефункциональные тесты
└── README.md                 # Этот файл
```

## Установка

```bash
pip install -r requirements.txt
```

## Запуск тестов

Все API тесты:
```bash
pytest tests/task_2_1_api/ -v
```

По категориям:
```bash
pytest tests/task_2_1_api/ -m positive -v
pytest tests/task_2_1_api/ -m negative -v
pytest tests/task_2_1_api/ -m e2e -v
pytest tests/task_2_1_api/ -m corner -v
pytest tests/task_2_1_api/ -m nonfunctional -v
```

## С Allure отчётом

```bash
pytest tests/task_2_1_api/ --alluredir=task_2_1_api/allure-results
allure serve task_2_1_api/allure-results
```

## Тест-кейсы

См. TESTCASES.md — секция "Тест-кейсы API"

## Линтер

```bash
ruff check tests/task_2_1_api/
```
