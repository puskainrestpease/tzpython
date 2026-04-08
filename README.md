# Тестовое Задание для effective mobile
Роль юзера хранится в users.role_id

- регистрация
- login
- logout
- профиль
- soft delete
- токен-аутентификация
- простая ACL-схема на ролях
- mock-ресурс `products`
- admin API для правил доступа

## Запросы

- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `PATCH /api/auth/me/`
- `DELETE /api/auth/me/`
- `GET /api/products/`
- `GET /api/products/<id>/`
- `GET /api/rules/` (admin)
- `POST /api/rules/` (admin)
- `PATCH /api/rules/<id>/` (admin)

нет токена -> `401 Unauthorized`
авторизован, прав нет -> `403 Forbidden`
права в таблице `access_rules`
