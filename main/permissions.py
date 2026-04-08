from .models import AccessRule


def is_admin(user) -> bool:
    return bool(user and user.role and user.role.slug == "admin")


def get_rule(user, element_slug: str):
    if not user or not user.role:
        return None
    return (
        AccessRule.objects
        .select_related("role", "element")
        .filter(role=user.role, element__slug=element_slug)
        .first()
    )


def can_do(user, element_slug: str, action: str, owner_id=None) -> bool:
    rule = get_rule(user, element_slug)
    if not rule:
        return False

    if action == "read":
        if rule.read_permission:
            return owner_id is None or owner_id == user.id
        return False

    if action == "create":
        return rule.create_permission

    if action == "update":
        return rule.update_permission and (owner_id is None or owner_id == user.id)

    if action == "delete":
        return rule.delete_permission and (owner_id is None or owner_id == user.id)

    return False
