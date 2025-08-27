<h2>🚀 Установка и запуск</h2>


<h4>
1. Создайте файл .env в корневой директории согласно .env.example
</h4>

```requirements
PROJECT_NAME=
SECRET_KEY=
DEBUG=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432

REDIS_PORT=6379
```

<h4>
2. Запустите docker compose:
</h4>

```commandline
docker compose up --build -d
```
<h4>
3. Создайте суперпользователя:
</h4>

```commandline
docker exec -it {PROJECT_NAME из .env}_web python manage.py createsuperuser
```
<h4>
4. Выполните тесты:
</h4>

```commandline
docker exec -it {PROJECT_NAME из .env}_web python manage.py test api
```

<br>

<b>Админ-панель:</b> <em>http://127.0.0.1/admin/</em><br>
<b>Список страниц:</b> <em>http://127.0.0.1/api/v1/pages/</em><br>