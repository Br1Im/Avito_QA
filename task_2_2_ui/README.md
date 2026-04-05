# Задание 2.2: Тесты UI

## Структура

```
task_2_2_ui/
├── conftest_ui.py     # Фикстуры Playwright
├── test_ui.py         # UI тесты
└── README.md         # Этот файл
```

## Установка

```bash
pip install -r requirements.txt
playwright install chromium
```

## Запуск тестов

Все UI тесты:
```bash
pytest tests/task_2_2_ui/ -v
```

По категориям:
```bash
pytest tests/task_2_2_ui/ -m desktop -v
pytest tests/task_2_2_ui/ -m mobile -v
```

## Тест-кейсы

См. TESTCASES.md — секция "UI Тест-кейсы"

## С Allure отчётом

```bash
pytest tests/task_2_2_ui/ --alluredir=task_2_2_ui/allure-results
allure serve task_2_2_ui/allure-results
```

## Примечание

UI тесты используют Playwright. Убедитесь, что Chromium установлен:
```bash
playwright install chromium
```
