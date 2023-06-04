## Кулинарное приложение Фудграм
![example workflow](https://github.com/kazakni/foodgram-project-react/actions/workflows/main.yml/badge.svg)
![alt text](https://sun9-55.userapi.com/impg/9aQjMO8FW8_uM-OLyiX9R-NaZWIzwxFbc7BrRA/ioj5uu1CPIk.jpg?size=1220x747&quality=95&sign=453cf36baf9aaa2da82c836e7585dc49&type=album)

### Описание:

Веб-приложение предназначено для создания, хранения кулинарных рецептов, подписки на интересных авторов.
Также приложение предоставляет возможность скачивать суммарное кол-во ингредиентов тех рецептов, которые пользователи добавили в свою корзину.

Автором репозитория реализован Бэкенд.

Стек:
- Django Rest Framework
- PostgreSQL
- NGINX
- Docker
- CI/CD Github actions
- Python 3.7 +


## Развертывание проекта

- Для локального развёртывания проекта необходимо клонировать текущий репозиторий:

```sh
git clone https://github.com/KazakNi/foodgram-project-react.git
```

- Перейти в папку infra:

```sh
cd infra
```
- Заполнить файл переменных окружения .env
- Поднять локально докер-контейнер:

```sh
docker-compose up -d
```

- Войти в контейнер бэкенда, создать суперюзера, подгрузить дамп ингредиентов в базу данных.

```sh
docker exec -it nikitakaz/foodgram:v1.0.0 bash
python manage.py createsuperuser
---создаем пользователя---
python manage.py loaddump data/data.json
```
Приложение будет доступно по адресу _localhost/recipes_

После входа в учетную запись можем наполнять сайт.
## License

MIT
