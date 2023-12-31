# task_list

Проект будет доступен по адресу http://127.0.0.1:8000/
Или http://0.0.0.0:8000/

Проект TaskList это список задач, которые необходимо обработать и дать ответ.

У задач есть следующие поля:
- Номер
- Статус
- Пользователь
- Дата создания
- Дата обновления

## Краткое описание функционала
- Задачи создает любой пользователь.
- Каждый пользователь может выполнять и просматривать только свои задачи. 
- Админу доступны все задачи.


## Технологии
- python 3.10
- django 3.2.19
- django_rest_framework 3.14.0
- celery 5.2.7
- redis 4.5.5
- PyJWT 2.7.0

#.env файл
В ./task_list/ проекта необходимо создать .env файл.
Разместите в нем следующие переменные:

- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=<Имя базы данных>
- POSTGRES_USER=<Имя базы пользователя>
- POSTGRES_PASSWORD=<Пароль базы данных>
- DB_HOST=db
- DB_PORT=<Порт базы данных>
- SECRET_KEY=<Секретный ключ Django>
- CELERY_BROKER=redis://redis:6379/0

## Чтобы развернуть проект
Клонировать репозиторий
```sh
git clone <ssh ссылка>
```
В дирректории проекта выполните комманду, для запуска контейнера
```sh
sudo docker compose up --build -d
```
Выполните миграции
```
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
```
Затем необходимо создать superuser 
```sh
sudo docker-compose exec web python manage.py createsuperuser
```
Перейти по адресу сервера
```sh
http://127.0.0.1:8000/
http://0.0.0.0:8000/
```

## Создание задач:
/api/v1/tasks/ пользователь отправляет POST запрос для создания задачи.
Никаких данных передавать не нужно


## Обработка задачи:
/api/v1/processing/ GET запрос вернет все задачи со статусом CREATE
/api/v1/processing/<id задачи>/ пользователь отправляет PATCH запрос для обновления статуса задачи.
Celery принимает задачу и спустя 10 секунд статус изменится.


## Ответ по задаче:
/api/v1/answer/<id задачи>/ GET запрос вернет все задачи со статусом PROCESSING
/api/v1/answer/<id задачи>/ пользователь отправляет PATCH запрос для обновления статуса задачи.
Celery принимает задачу и спустя 10 секунд статус изменится.

## Удаление задач
- Каждый день, в 1 час ночи Celery запускает таску, которая удаляет стары задачи
- Старые задачи это задачи со статусом ANSWER, обновление которых произошло более 14 дней назад  

## Регистрация пользователя:
1. /api/v1/auth/signup/ пользователь отправляет POST запрос с параметрами 
email и username и password для регистрации - обязательные поля. Так же есть first_name и last_name.
2. /api/v1/auth/token/ пользователь отправляет POST-запрос с параметрами 
username и password на эндпоинт. В ответ ему приходит token (JWT-токен).
3. /api/v1/users/me/ GET запрос вернет информацию о пользователе
4. /api/v1/users/me/ по данному энтпоинту пользователь может отправить PATCH
запрос и заполнить поля в своём профайле, или Get запросом просмотреть информацию о себе


## Тесты
- необходимо перейти в корневую директорию проекта где расположен файл ```manage.py```
- запустить тесты - ввести команду ```python -m unittest task_list.api.tests```

## Автор 
# Григорян Арсен