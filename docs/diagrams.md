# Диаграммы

## Бизнес-контекст

```mermaid
flowchart LR
    Guest["Гость"] --> Catalog["Каталог"]
    User["Пользователь"] --> Order["Заказ"]
    User --> Review["Отзывы"]
    User --> Favorite["Избранное"]
    Admin["Администратор"] --> Manage["Управление справочниками"]
```

## Use Case

```mermaid
flowchart TB
    Guest["Гость"] --> Browse["Просмотр каталога"]
    Guest --> Search["Поиск по названию"]
    Guest --> Filter["Фильтр по категории"]
    User["Пользователь"] --> Cart["Корзина"]
    User --> Checkout["Оформить заказ"]
    User --> Pay["Оплатить условно"]
    User --> Track["Отследить статус"]
    User --> Reviews["Оставить отзыв"]
    User --> Favorites["Избранное"]
    Admin["Администратор"] --> Crud["CRUD Category и Pizza"]
```

## Концептуальная модель классов

```mermaid
classDiagram
    User "1" --> "*" Order
    User "1" --> "*" Review
    User "1" --> "*" Favorite
    Category "1" --> "*" Pizza
    Order "1" --> "*" OrderItem
    Pizza "1" --> "*" OrderItem
    Pizza "1" --> "*" Review
    Pizza "1" --> "*" Favorite
```

## Компоненты

```mermaid
flowchart LR
    React["React SPA"] --> API["Django REST Framework"]
    React --> WS["Channels WebSocket"]
    API --> SQLite["SQLite"]
    API --> JWT["Simple JWT"]
    API --> Admin["Django Admin"]
    API --> Thread["Backend status thread"]
    Thread --> WS
```

## JWT

```mermaid
sequenceDiagram
    participant React
    participant API
    React->>API: POST /api/auth/login/
    API-->>React: access + refresh
    React->>API: GET /api/auth/profile/ with Bearer token
    API-->>React: profile
```

## WebSocket status

```mermaid
sequenceDiagram
    participant React
    participant API
    participant Thread
    participant WS
    React->>API: POST /api/orders/{id}/pay/
    API->>WS: paid
    API->>Thread: start
    Thread->>WS: cooking
    Thread->>WS: baking
    Thread->>WS: delivering
    Thread->>WS: completed
    WS-->>React: status updates
```

## Примечания

Нормализация БД не выполняется по уточненному требованию. Docker не используется. Используется SQLite. В backend ровно два приложения: `users` и `pizzeria`. Модель пользователя расширенная. API использует JWT. Доступ разделен на гостя, авторизованного пользователя и администратора.
