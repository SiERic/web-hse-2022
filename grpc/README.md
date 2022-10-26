# grpc-python-example
________________________________________________________________________________________
* gRPC-сервер принимает в запросе пол и континент и генерирует жабу с соответствующим видом и именем.

* FastApi-сервер принимает пустой запрос, случайно выбирает пол и континент и идёт с таким запросом в первый сервис, возвращая случайную лягушку


## Подготовка


### venv установка зависимостей
```bash
virtualenv --python=python3.8 .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```


### Компиляция .proto-файлов (при необходимости)
Compile the .proto files...
```
python -m grpc_tools.protoc -I definitions/ --python_out=definitions/builds/ --grpc_python_out=definitions/builds/ definitions/service.proto
```


## Запуск серверов
```
python grpc_server.py -p 3000 
python fastapi_server.py -p 3001
```

## Запросы

Запрос к grpc-серверу через клиент можно сделать так:
```bash
python3 client.py -g Male -c Asia
```

Запрос к FastApi-серверу можно сделать так:
```bash
curl localhost:3001/generate_frog
```

## Тестирование

### Юнит-тесты

```bash
python3 -m pytest test.py -v -m unittest
```

### Функциональные тесты

Сначала нужно запустить серверы (см. предыдущий пункт)

Затем запустить
```bash
python3 -m pytest test.py -v -m functional
```