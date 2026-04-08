# Тестовое Задание для effective mobile
Роль юзера хранится в users.role_id

Поля доступа:
- read_permission - можно читать собственные объекты
- read_all_permission - можно читать все объекты
- create_permission - можно создавать
- update_permission - можно редактировать собственные объекты
- update_all_permission - можно редактировать все объекты
- delete_permission - можно удалять собственные объекты
- delete_all_permission - можно удалять все объекты

если юзер не авторизован ошибка 401, без прав правки (с входом) 403
если данные (обьект) принадлежит/ат пользователю, проверка own-permission
*_all_permission - доступ всем обьектам
