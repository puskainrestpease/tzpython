# Примеры запросов

## Login
POST /api/accounts/login/
```json
{
  "email": "admin@test.com",
  "password": "admin123"
}
```

## Me
GET /api/accounts/me/
Header:
Authorization: Bearer <token>
