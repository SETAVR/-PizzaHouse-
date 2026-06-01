# PizzaHouse

Учебное веб-приложение пиццерии по варианту "Кулинария". Основная сущность - `Pizza`, модель категории - `Category`.

## Стек

Backend: Python, Django, Django REST Framework, Simple JWT, django-cors-headers, Channels, Daphne, Pillow, SQLite.

Frontend: React, React Router, Axios, обычный CSS, `localStorage`.

Не используются Docker, PostgreSQL, Redis, Celery, Redux, React Query, Tailwind и backend-модель корзины.

## Структура

```text
backend/
  config/
  users/
  pizzeria/
  manage.py
  requirements.txt
frontend/
  src/
  package.json
docs/
  stage_0_report.md
  architecture.md
  api_specification.md
  jwt_scheme.md
  ui_api_interaction.md
  diagrams.md
```

## Запуск backend на Windows

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data
python manage.py runserver
```

Backend будет доступен на `http://localhost:8000/`.

## Запуск frontend на Windows

В отдельном терминале:

```powershell
cd frontend
npm install
npm run dev
```

Frontend будет доступен на `http://localhost:5173/`.

## Миграции

Начальные миграции уже добавлены. Если модели менялись:

```powershell
cd backend
.\.venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
```

## Demo data

Команда:

```powershell
python manage.py seed_data
```

Создает категории "Классические", "Острые", "Мясные", "Вегетарианские" и несколько пицц: "Маргарита", "Пепперони", "Четыре сыра", "Мясная", "Вегетарианская".

## API endpoints

Auth:

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/profile/`
- `PUT/PATCH /api/auth/profile/`

Category CRUD:

- `GET /api/categories/`
- `GET /api/categories/{id}/`
- `POST /api/categories/`
- `PATCH /api/categories/{id}/`
- `DELETE /api/categories/{id}/`

Pizza CRUD:

- `GET /api/pizzas/`
- `GET /api/pizzas/{id}/`
- `POST /api/pizzas/`
- `PATCH /api/pizzas/{id}/`
- `DELETE /api/pizzas/{id}/`

Reviews:

- `GET /api/pizzas/{id}/reviews/`
- `POST /api/pizzas/{id}/reviews/`

Favorites:

- `GET /api/favorites/my/`
- `POST /api/favorites/toggle/`

Orders:

- `POST /api/orders/`
- `GET /api/orders/my/`
- `GET /api/orders/{id}/`
- `POST /api/orders/{id}/pay/`

## WebSocket

Адрес:

```text
ws://localhost:8000/ws/orders/{order_id}/
```

Используется только для real-time обновления статуса заказа. После `POST /api/orders/{id}/pay/` backend запускает `threading.Thread` и последовательно отправляет статусы:

```text
paid -> cooking -> baking -> delivering -> completed
```

React не меняет статус через `setTimeout`, а только принимает сообщения от backend.

## Сценарий демонстрации

1. Зарегистрироваться.
2. Войти.
3. Открыть каталог.
4. Найти пиццу по названию.
5. Отфильтровать по категории.
6. Открыть детальную страницу через "Подробнее".
7. Добавить пиццу в корзину.
8. Изменить количество в корзине.
9. Удалить позицию из корзины.
10. Оформить заказ.
11. Нажать "Оплатить условно".
12. Дождаться real-time изменения статуса через WebSocket.
13. Добавить пиццу в избранное.
14. Открыть избранное.
15. Добавить отзыв.

## Что проверить вручную

- Регистрация, вход и профиль.
- CRUD `Category` и `Pizza` под администратором.
- Поиск пицц только по названию.
- Фильтр по категории и пагинацию.
- Корзину после перезагрузки страницы.
- Создание заказа из корзины.
- Real-time статусы заказа после условной оплаты.
- Добавление и удаление избранного.
- Создание и просмотр отзывов.
