# Foodgram

## Описание проекта

**Foodgram** - это проект, представляющий собой онлайн-сервис и API для публикации и обмена рецептами. Пользователи могут публиковать свои рецепты, подписываться на других пользователей, добавлять понравившиеся рецепты в список «Избранное», а также скачивать сводный список продуктов, необходимых для приготовления выбранных блюд.

## Основные особенности проекта Foodgram:

 - Публикация рецептов: Пользователи могут публиковать свои рецепты, добавляя ингредиенты, количество и измерения.
 - Подписка: Пользователи могут подписываться на других пользователей.
- Список «Избранное»: Пользователи могут добавлять понравившиеся рецепты в свой список «Избранное».
- Сводный список продуктов: Перед походом в магазин пользователи могут скачать сводный список продуктов, необходимых для приготовления выбранных блюд.
- API: Проект реализован на Django и DjangoRestFramework, и предоставляет API для взаимодействия с данными.
- Проект развернут на Docker-контейнерах и доступен через API-интерфейс. Документация к API написана с использованием Redoc.

## API

1. Пользователи:
   - `GET /api/users/` - Список пользователей
   - `POST /api/users/` - Регистрация пользователя
   - `GET /api/users/{id}/` - Профиль пользователя
   - `GET /api/users/me/` - Текущий пользователь
   - `PUT /api/users/me/avatar/` - Добавление аватара
   - `DELETE /api/users/me/avatar/` - Удаление аватара
   - `POST /api/users/set_password/` - Изменение пароля

2. Теги:
   - `GET /api/tags/` - Список тегов
   - `GET /api/tags/{id}/` - Получение тега

3. Рецепты:
   - `GET /api/recipes/` - Список рецептов
   - `POST /api/recipes/` - Создание рецепта
   - `GET /api/recipes/{id}/` - Получение рецепта
   - `PATCH /api/recipes/{id}/` - Обновление рецепта
   - `DELETE /api/recipes/{id}/` - Удаление рецепта
   - `GET /api/recipes/{id}/get-link/` - Получить короткую ссылку на рецепт

4. Избранное:
   - `POST /api/recipes/{id}/favorite/` - Добавить рецепт в избранное
   - `DELETE /api/recipes/{id}/favorite/` - Удалить рецепт из избранного

5. Список покупок:
   - `POST /api/recipes/{id}/shopping_cart/` - Добавить рецепт в список покупок
   - `DELETE /api/recipes/{id}/shopping_cart/` - Удалить рецепт из списка покупок
   - `GET /api/recipes/download_shopping_cart/` - Скачать список покупок

6. Подписки:
   - `GET /api/users/subscriptions/` - Мои подписки
   - `POST /api/users/{id}/subscribe/` - Подписаться на пользователя
   - `DELETE /api/users/{id}/subscribe/` - Отписаться от пользователя

7. Ингредиенты:
   - `GET /api/ingredients/` - Список ингредиентов
   - `GET /api/ingredients/{id}/` - Получение ингредиента

8. Аутентификация:
   - `POST /api/auth/token/login/` - Получить токен авторизации
   - `POST /api/auth/token/logout/` - Удаление токена

## Запуск проекта

- клонируйте репозитарий 
```bash
git clone https://github.com/YroslavBochkov/foodgram.git
cd backend
```
### Создайте и активируйте виртуальное окружение:
#### Для Linux/macOS:
```bash
python3 -m venv env
source env/bin/activate
```
#### Для Windows:
```bash
python3 -m venv env
source env/scripts/activate
```
#### 3. Обновите pip и установите зависимости:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
### Сформируйте базу данных:
#### Измените DATABASES в settings.py для использования SQLite:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
### Примените миграции:
```bash
python3 manage.py migrate
```
#### 6. Запустите проект на локальном сервере:
```bash
python3 manage.py runserver
```

## Технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Примеры запросов

 - Список пользователей:

 ```http request
### Все пользователи
GET http://127.0.0.1:8080/api/users/

### С учетом лимита
GET http://127.0.0.1:8080/api/users/?limit=1
```

### Регистрация пользователя:

```http request
POST http://127.0.0.1:8080/api/users/
{
    "email": "email@email.ru",
    "username": "username",
    "first_name": "Вася",
    "last_name": "Иванов",
    "password": "password"
}
```

### Список тегов:

```http request
GET http://127.0.0.1:8080/api/tags/
```
 ### Список ингредиентов:

 ```http request
### Получить список
GET http://127.0.0.1:8080/api/ingredients/

### Фильтр по имени
GET http://127.0.0.1:8080/api/ingredients/?name={{ingredientNameFirstLatter}}

### По ID
GET http://127.0.0.1:8080/api/ingredients/{{IndredientId}}/
```


### Автор

Ярослав Бочков