# Generated by Django 4.2.3 on 2023-07-26 17:59

import backend.account.utils
import backend.account.validators
from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserBase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="first_name"),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="last_name"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        max_length=13,
                        unique=True,
                        validators=[
                            backend.account.validators.validate_uzb_phone_number
                        ],
                        verbose_name="phone_number",
                    ),
                ),
                ("phone_token", models.CharField(blank=True, max_length=6, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CUSTOMER", "Customer"),
                            ("ADMINISTRATOR", "Administrator"),
                        ],
                        default="CUSTOMER",
                        max_length=15,
                        verbose_name="status",
                    ),
                ),
                (
                    "avatar",
                    django_resized.forms.ResizedImageField(
                        crop=None,
                        default="avatars/no_photo.png",
                        force_format="WEBP",
                        keep_meta=True,
                        quality=100,
                        scale=1.0,
                        size=[1920, 1080],
                        upload_to=backend.account.utils.generate_unique_filename,
                        verbose_name="avatar",
                    ),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="format: Y-m-d H:M:S",
                        verbose_name="date user created",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="format: Y-m-d H:M:S",
                        verbose_name="date user last updated",
                    ),
                ),
                (
                    "expires_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="expiry time of token"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Accounts",
                "verbose_name_plural": "Accounts",
            },
        ),
    ]
