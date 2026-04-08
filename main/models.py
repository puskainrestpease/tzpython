import uuid
import bcrypt
from datetime import timedelta

from django.db import models
from django.utils import timezone


class Role(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.slug


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, default="")
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password: str):
        self.password_hash = bcrypt.hashpw(
            raw_password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.checkpw(
            raw_password.encode("utf-8"),
            self.password_hash.encode("utf-8"),
        )

    def __str__(self):
        return self.email


class SessionToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_for_user(cls, user, hours=24 * 7):
        return cls.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(hours=hours),
        )

    def __str__(self):
        return str(self.token)


class BusinessElement(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.slug


class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)

    read_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = ("role", "element")

    def __str__(self):
        return f"{self.role.slug} - {self.element.slug}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
