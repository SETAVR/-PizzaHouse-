# 🍕PizzaHouse🍕

**PizzaHouse** - учебное веб-приложение пиццерии, разработанное для курсового проекта по дисциплине "Технология разработки программного обеспечения".

Проект относится к варианту **"Кулинария"**. Основная сущность предметной области - `Pizza`, справочник категорий - `Category`.

Приложение позволяет пользователю просматривать каталог пицц, искать пиццу по названию, фильтровать каталог по категории, добавлять позиции в корзину, оформлять заказ, условно оплачивать его, отслеживать статус заказа в реальном времени через WebSocket, добавлять пиццы в избранное и оставлять отзывы.

Проект выполнен по требованиям **траектории В**: Django REST API, React SPA, JWT-аутентификация и WebSocket. При этом проект намеренно остается учебным MVP и не перегружается промышленными технологиями.

## 📄 Пояснительная записка 
- [Скачать пояснительную записку](./Kursovoy_proekt_PizzaHouse(5).docx?raw=1)

---

## Технологический стек

### Backend

- **Python** - язык разработки backend-части.
- **Django** - основной web-фреймворк.
- **Django REST Framework** - реализация REST API.
- **djangorestframework-simplejwt** - JWT-аутентификация через access и refresh token.
- **Django Channels** - WebSocket-слой для real-time статуса заказа.
- **Daphne** - ASGI runtime для локального запуска Channels.
- **django-cors-headers** - настройка CORS для связки Django + React.
- **Pillow** - работа с изображениями.
- **SQLite** - учебная база данных без отдельного сервера.

### Frontend

- **React** - интерфейс одностраничного приложения.
- **Vite** - сборка и dev-сервер frontend.
- **React Router** - маршрутизация между страницами SPA.
- **Axios** - HTTP-клиент для запросов к REST API.
- **Обычный CSS** - стили без Tailwind и CSS-фреймворков.
- **localStorage** - хранение JWT-токенов и корзины на клиенте.

### Что специально не используется

- Docker.
- PostgreSQL.
- Redis.
- Celery.
- Redux.
- React Query.
- Tailwind.
- Backend-модель корзины.

Корзина реализована на стороне React и отправляется на backend только при оформлении заказа.

---

## Основной функционал

### Публичная часть

- Просмотр каталога пицц.
- Просмотр категорий.
- Детальная страница пиццы.
- Поиск пиццы только по названию.
- Фильтрация пицц по категории.
- Пагинация каталога.
- Просмотр отзывов.

### Авторизованный пользователь

- Регистрация и вход по JWT.
- Просмотр и редактирование профиля.
- Добавление пицц в корзину.
- Изменение количества позиций в корзине.
- Удаление позиций из корзины.
- Оформление заказа из корзины.
- Просмотр своих заказов.
- Условная оплата заказа.
- Real-time отслеживание статуса заказа через WebSocket.
- Добавление и удаление избранного.
- Просмотр избранных пицц.
- Добавление отзывов с рейтингом от 1 до 5.

### Администратор

- Полный CRUD для `Category`.
- Полный CRUD для `Pizza`.
- Управление пользователями, заказами, отзывами и избранным через Django Admin.

---

## Структура проекта

```text
backend/
  config/                         # Настройки Django, ASGI, WSGI и корневые URL
  users/                          # Пользователи, профиль, регистрация, JWT
  pizzeria/                       # Категории, пиццы, заказы, отзывы, избранное, WebSocket
  manage.py
  requirements.txt

frontend/
  public/
    pizzas/                       # Изображения демо-пицц
  src/
    api/                          # Axios client
    components/                   # Переиспользуемые компоненты
    context/                      # AuthContext и CartContext
    pages/                        # Страницы приложения
    utils/                        # Вспомогательные функции
    App.jsx
    main.jsx
    styles.css
  package.json
  vite.config.js

docs/
  stage_0_report.md
  architecture.md
  api_specification.md
  jwt_scheme.md
  ui_api_interaction.md
  diagrams.md
```

---

## Установка и запуск

### Требования

- Python 3.10+.
- Node.js 18+.
- npm.

### 1. Запуск backend на Windows

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

Backend будет доступен по адресу:

```text
http://localhost:8000/
```

Django Admin:

```text
http://localhost:8000/admin/
```

### 2. Запуск frontend на Windows

В отдельном терминале:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Frontend будет доступен по адресу:

```text
http://localhost:5173/
```

Если в PowerShell запрещен запуск `npm.ps1`, используйте именно `npm.cmd`, как указано выше.

---

## Миграции и демо-данные

Начальные миграции уже есть в проекте. Если модели были изменены:

```powershell
cd backend
.\.venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
```

Для заполнения базы демо-данными:

```powershell
python manage.py seed_data
```

Команда создает категории:

- Классические.
- Острые.
- Мясные.
- Вегетарианские.

И демо-пиццы:

- Маргарита.
- Пепперони.
- Четыре сыра.
- Мясная.
- Вегетарианская.

Изображения этих пицц находятся в `frontend/public/pizzas/`.

---

## REST API

Базовый адрес API:

```text
http://localhost:8000/api/
```

### Auth

| Метод | Endpoint | Назначение |
| --- | --- | --- |
| POST | `/api/auth/register/` | Регистрация пользователя |
| POST | `/api/auth/login/` | Получение access и refresh token |
| POST | `/api/auth/token/refresh/` | Обновление access token |
| GET | `/api/auth/profile/` | Просмотр профиля |
| PUT/PATCH | `/api/auth/profile/` | Редактирование профиля |

### Categories

| Метод | Endpoint | Назначение |
| --- | --- | --- |
| GET | `/api/categories/` | Список категорий |
| GET | `/api/categories/{id}/` | Детали категории |
| POST | `/api/categories/` | Создание категории, только админ |
| PATCH | `/api/categories/{id}/` | Обновление категории, только админ |
| DELETE | `/api/categories/{id}/` | Удаление категории, только админ |

### Pizzas

| Метод | Endpoint | Назначение |
| --- | --- | --- |
| GET | `/api/pizzas/` | Список пицц с пагинацией |
| GET | `/api/pizzas/?search=...` | Поиск по названию |
| GET | `/api/pizzas/?category=1` | Фильтрация по категории |
| GET | `/api/pizzas/{id}/` | Детальная страница пиццы |
| POST | `/api/pizzas/` | Создание пиццы, только админ |
| PATCH | `/api/pizzas/{id}/` | Обновление пиццы, только админ |
| DELETE | `/api/pizzas/{id}/` | Удаление пиццы, только админ |

### Reviews

| Метод | Endpoint | Назначение |
| --- | --- | --- |
| GET | `/api/pizzas/{id}/reviews/` | Просмотр отзывов к пицце |
| POST | `/api/pizzas/{id}/reviews/` | Добавление отзыва, нужен JWT |

### Favorites

| Метод | Endpoint | Назначение |
| --- | --- | --- |
| GET | `/api/favorites/my/` | Просмотр избранного, нужен JWT |
| POST | `/api/favorites/toggle/` | Добавление или удаление пиццы из избранного, нужен JWT |

Пример тела запроса:

```json
{
  "pizza_id": 1
}
```

### Orders

| Метод | Endpoint | Назначение |
| --- | --- | --- |
| POST | `/api/orders/` | Создание заказа, нужен JWT |
| GET | `/api/orders/my/` | Просмотр своих заказов, нужен JWT |
| GET | `/api/orders/{id}/` | Детали своего заказа, нужен JWT |
| POST | `/api/orders/{id}/pay/` | Условная оплата заказа, нужен JWT |

Пример создания заказа:

```json
{
  "phone": "+79990000000",
  "address": "Ставрополь, ул. Учебная, 1",
  "items": [
    {
      "pizza_id": 1,
      "quantity": 2
    }
  ]
}
```

Backend сам рассчитывает `total_price` по актуальным ценам пицц.

---

## WebSocket

WebSocket используется только для real-time обновления статуса заказа.

Адрес подключения:

```text
ws://localhost:8000/ws/orders/{order_id}/
```

Сценарий:

1. Пользователь создает заказ через `POST /api/orders/`.
2. React открывает страницу заказа и подключается к WebSocket.
3. Пользователь нажимает "Оплатить условно".
4. Backend обрабатывает `POST /api/orders/{id}/pay/`.
5. Backend устанавливает `is_paid = true` и `status = paid`.
6. Backend запускает `threading.Thread`.
7. Поток последовательно меняет статусы:

```text
paid -> cooking -> baking -> delivering -> completed
```

8. После каждой смены backend отправляет WebSocket-сообщение.
9. React только принимает сообщения и обновляет интерфейс.

React не меняет статус заказа через `setTimeout`.

---

## Документация проекта

В папке `docs/` находятся:

- `stage_0_report.md` - отчет этапа 0.
- `architecture.md` - описание архитектуры.
- `api_specification.md` - спецификация API.
- `jwt_scheme.md` - схема JWT-аутентификации.
- `ui_api_interaction.md` - взаимодействие UI и API.
- `diagrams.md` - Mermaid-диаграммы.

Также есть отдельный Word-файл:

```text
Документация WebSocket и требования траектории В.docx
```

Он кратко описывает WebSocket и требования траектории В, использованные в проекте.

---

## Проверка проекта вручную

Рекомендуемый сценарий демонстрации:

1. Зарегистрироваться.
2. Войти.
3. Открыть каталог.
4. Выполнить поиск пиццы по названию.
5. Отфильтровать каталог по категории.
6. Открыть детальную страницу пиццы.
7. Добавить пиццу в корзину.
8. Изменить количество в корзине.
9. Удалить позицию из корзины.
10. Оформить заказ.
11. Нажать "Оплатить условно".
12. Дождаться real-time изменения статуса через WebSocket.
13. Добавить пиццу в избранное.
14. Открыть избранное.
15. Добавить отзыв.

---

## Автотесты

В проект добавлены базовые backend-тесты для приложения `pizzeria`. Они проверяют ключевые сценарии:

- гость может просматривать список пицц;
- гость не может создавать пиццу через CRUD API;
- авторизованный пользователь может создать заказ;
- backend сам рассчитывает итоговую сумму заказа;
- избранное добавляется и удаляется через toggle endpoint;
- условная оплата переводит заказ в статус `paid` и запускает backend-сценарий обновления статуса.

Запуск тестов:

```powershell
cd backend
.\.venv\Scripts\activate
python manage.py test pizzeria
```

Расширенный запуск с измерением покрытия:

```powershell
cd backend
python -m coverage erase
python -m coverage run manage.py test users pizzeria
python -m coverage report -m
```

Контрольный результат: 11 успешно выполненных тестов и 86% покрытия прикладного backend-кода. Подробности приведены в `docs/testing_coverage.md`.

## Интерактивная документация API

После запуска backend доступны:

- Swagger UI: `http://localhost:8000/api/docs/`;
- ReDoc: `http://localhost:8000/api/redoc/`;
- OpenAPI schema: `http://localhost:8000/api/schema/`.


