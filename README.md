# ТЗ Sber - калькулятор депозита

Сервис представляет из себя калькулятор депозита, принимающий значения даты начала, суммы, ставки и периода, 
и возвращающий изменения депозитного счёта в дни начисления процентов 


## Запуск
```bash
docker build . -t deposit-calc
docker run -d -p 8001:8001 deposit-calc
```
## Проверка кода

### Линтер
```bash
ruff check
```
### Типизация
```bash
mypy app
```
### Тесты
```bash
pytest
```
### Покрытие
```bash
coverage run -m pytest
coverage report
```

## Документация API
http://localhost:8001/docs/