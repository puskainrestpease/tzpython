from django.core.management.base import BaseCommand
from main.models import Role, BusinessElement, AccessRule, User, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(slug="admin", defaults={"name": "Administrator"})
        user_role, _ = Role.objects.get_or_create(slug="user", defaults={"name": "User"})
        guest_role, _ = Role.objects.get_or_create(slug="guest", defaults={"name": "Guest"})

        products, _ = BusinessElement.objects.get_or_create(slug="products", defaults={"name": "Products"})
        rules_el, _ = BusinessElement.objects.get_or_create(slug="access_rules", defaults={"name": "Access rules"})

        AccessRule.objects.update_or_create(
            role=admin_role,
            element=products,
            defaults={
                "read_permission": True,
                "create_permission": True,
                "update_permission": True,
                "delete_permission": True,
            },
        )
        AccessRule.objects.update_or_create(
            role=user_role,
            element=products,
            defaults={
                "read_permission": True,
                "create_permission": True,
                "update_permission": True,
                "delete_permission": False,
            },
        )
        AccessRule.objects.update_or_create(
            role=guest_role,
            element=products,
            defaults={
                "read_permission": False,
                "create_permission": False,
                "update_permission": False,
                "delete_permission": False,
            },
        )

        AccessRule.objects.update_or_create(
            role=admin_role,
            element=rules_el,
            defaults={
                "read_permission": True,
                "create_permission": True,
                "update_permission": True,
                "delete_permission": True,
            },
        )

        admin, _ = User.objects.get_or_create(
            email="admin@test.com",
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "middle_name": "",
                "role": admin_role,
                "is_active": True,
                "password_hash": "",
            },
        )
        if not admin.password_hash:
            admin.set_password("admin123")
            admin.save()

        user, _ = User.objects.get_or_create(
            email="user@test.com",
            defaults={
                "first_name": "Test",
                "last_name": "User",
                "middle_name": "",
                "role": user_role,
                "is_active": True,
                "password_hash": "",
            },
        )
        if not user.password_hash:
            user.set_password("user123")
            user.save()

        Product.objects.get_or_create(name="Laptop", owner=user)
        Product.objects.get_or_create(name="Mouse", owner=user)
        Product.objects.get_or_create(name="Admin Product", owner=admin)

        self.stdout.write(self.style.SUCCESS("Demo data created"))
