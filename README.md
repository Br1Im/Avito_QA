# Avito QA Internship - Тестовый набор

## Структура проекта

```
.
├── task_2_1_api/              # Задание 2.1: Тесты API
│   ├── api_client.py
│   ├── conftest.py
│   ├── test_api_positive.py
│   ├── test_api_negative.py
│   ├── test_api_e2e.py
│   ├── test_api_nonfunctional.py
│   └── README.md
│
├── task_2_2_ui/              # Задание 2.2: UI тесты
│   ├── conftest_ui.py
│   ├── test_ui.py
│   └── README.md
│
├── TESTCASES.md               # Все тест-кейсы
├── BUGS.md                   # Баг-репорты
├── pytest.ini                 # Конфигурация pytest
├── pyproject.toml            # Конфигурация ruff
└── README.md                 # Этот файл
```

## Быстрый старт

### Установка зависимостей

```bash
pip install -r requirements.txt
playwright install chromium
```

## Задание 2.1: API тесты

См. [task_2_1_api/README.md](task_2_1_api/README.md)

```bash
pytest task_2_1_api/ -v
```

## Задание 2.2: UI тесты

См. [task_2_2_ui/README.md](task_2_2_ui/README.md)

```bash
pytest task_2_2_ui/ -v
```

## Allure отчёты

```bash
# API
pytest task_2_1_api/ --alluredir=task_2_1_api/allure-results
allure serve task_2_1_api/allure-results

# UI
pytest task_2_2_ui/ --alluredir=task_2_2_ui/allure-results
allure serve task_2_2_ui/allure-results
```

## Линтер

```bash
ruff check task_2_1_api/
```
