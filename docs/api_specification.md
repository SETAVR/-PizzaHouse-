# API specification

Базовый адрес: `http://localhost:8000/api/`

JWT передается в заголовке `Authorization: Bearer <access_token>`.

| Endpoint | Method | Назначение | Доступ |
| --- | --- | --- | --- |
| `/api/auth/register/` | POST | Регистрация | Гость |
| `/api/auth/login/` | POST | Получить access и refresh token | Гость |
| `/api/auth/token/refresh/` | POST | Обновить access token | Гость |
| `/api/auth/profile/` | GET | Получить профиль | Пользователь |
| `/api/auth/profile/` | PUT/PATCH | Обновить профиль | Пользователь |
| `/api/categories/` | GET | Список категорий | Все |
| `/api/categories/{id}/` | GET | Детали категории | Все |
| `/api/categories/` | POST | Создать категорию | Администратор |
| `/api/categories/{id}/` | PATCH | Изменить категорию | Администратор |
| `/api/categories/{id}/` | DELETE | Удалить категорию | Администратор |
| `/api/pizzas/` | GET | Список пицц с пагинацией | Все |
| `/api/pizzas/?search=...` | GET | Поиск только по `title` | Все |
| `/api/pizzas/?category=1` | GET | Фильтрация по категории | Все |
| `/api/pizzas/{id}/` | GET | Детали пиццы | Все |
| `/api/pizzas/` | POST | Создать пиццу | Администратор |
| `/api/pizzas/{id}/` | PATCH | Изменить пиццу | Администратор |
| `/api/pizzas/{id}/` | DELETE | Удалить пиццу | Администратор |
| `/api/pizzas/{id}/reviews/` | GET | Отзывы к пицце | Все |
| `/api/pizzas/{id}/reviews/` | POST | Добавить отзыв | Пользователь |
| `/api/favorites/my/` | GET | Мое избранное | Пользователь |
| `/api/favorites/toggle/` | POST | Добавить или удалить избранное | Пользователь |
| `/api/orders/` | POST | Создать заказ из корзины | Пользователь |
| `/api/orders/my/` | GET | Мои заказы | Пользователь |
| `/api/orders/{id}/` | GET | Детали своего заказа | Пользователь |
| `/api/orders/{id}/pay/` | POST | Условно оплатить заказ | Пользователь |

## Создание заказа

```json
{
  "phone": "+79990000000",
  "address": "Москва, учебная 1",
  "items": [
    { "pizza_id": 1, "quantity": 2 }
  ]
}
```

Backend сам рассчитывает `total_price` по актуальным ценам пицц и создает `OrderItem`.

## WebSocket

Адрес: `ws://localhost:8000/ws/orders/{order_id}/`

Сообщение:

```json
{
  "status": "cooking",
  "is_paid": true
}
```
