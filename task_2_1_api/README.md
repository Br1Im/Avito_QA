# API тесты (Задание 2.1)

## Файлы

- `api_client.py` — обёртка над requests
- `conftest.py` — фикстуры
- `test_api_positive.py` — позитивные тесты
- `test_api_negative.py` — негативные тесты
- `test_api_e2e.py` — E2E и корнер-кейсы
- `test_api_nonfunctional.py` — производительность, CORS

## Запуск

```bash
pytest task_2_1_api/ -v
```

С маркерами:
```bash
pytest task_2_1_api/ -m positive -v
pytest task_2_1_api/ -m negative -v
pytest task_2_1_api/ -m e2e -v
pytest task_2_1_api/ -m nonfunctional -v
```

## Allure

```bash
pytest task_2_1_api/ --alluredir=task_2_1_api/allure-results
allure serve task_2_1_api/allure-results
```
