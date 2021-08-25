# API сервиса Yatube

## Стек технологий
python3, Django Rest Framework, sqlite, simpleJWT, Django-filter

## Для запуска проекта:
1. Проверьте установлен ли интерпретатор Python.
2. Клонируйте репозиторий и перейдите в папку проекта, для этого в консоли наберите:
    ```
    git clone https://github.com/SRSamoylenko/hw05_final
    cd hw05_final
    ```
3. Создайте и активируйте виртуальное окружение:
    ```
    python3 -m venv venv
    source ./venv/bin/activate
    ```
4. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
5. Выполните миграции:
    ```
    python manage.py migrate
    ```
7. Для запуска приложения используйте:
    ```
    python manage.py runserver
    ```
6. Приложение доступно по адресу: `http://127.0.0.1:8000/`.

## Как пользоваться
Документация по проекту будет доступна по ссылке `http://127.0.0.1:8000/redoc`
