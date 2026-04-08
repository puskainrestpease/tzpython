from django.db import migrations, models
import django.db.models.deletion
import uuid
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BusinessElement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True)),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(unique=True)),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("middle_name", models.CharField(blank=True, default="", max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password_hash", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("role", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="main.role")),
            ],
        ),
        migrations.CreateModel(
            name="SessionToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("expires_at", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sessions", to="main.user")),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to="main.user")),
            ],
        ),
        migrations.CreateModel(
            name="AccessRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("read_permission", models.BooleanField(default=False)),
                ("create_permission", models.BooleanField(default=False)),
                ("update_permission", models.BooleanField(default=False)),
                ("delete_permission", models.BooleanField(default=False)),
                ("element", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="main.businesselement")),
                ("role", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="main.role")),
            ],
            options={
                "unique_together": {("role", "element")},
            },
        ),
    ]
