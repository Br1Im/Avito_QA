Задание 2.2 - UI тесты

## Файлы

- `conftest_ui.py` - фикстуры Playwright, настройки viewport
- `test_ui.py` - UI тесты: фильтры, сортировка, тема, статистика

## Запуск

```bash
pytest task_2_2_ui/ -v
```

По категориям:
```bash
pytest task_2_2_ui/ -m desktop -v
pytest task_2_2_ui/ -m mobile -v
```

## Allure

```bash
pytest task_2_2_ui/ --alluredir=task_2_2_ui/allure-results
allure serve task_2_2_ui/allure-results
```
