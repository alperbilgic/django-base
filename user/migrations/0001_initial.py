# Generated by Django 4.2.11 on 2024-04-15 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import user.models
import utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("common", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Avatar",
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
                ("image", models.CharField(max_length=2048, null=True)),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
            ],
            options={
                "db_table": "avatar",
            },
        ),
        migrations.CreateModel(
            name="Locale",
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
                ("name", models.CharField(max_length=150, unique=True)),
                ("code", models.CharField(default="tr", max_length=16, unique=True)),
                (
                    "created",
                    utils.fields.DateTimeWithoutTZField(auto_now_add=True, null=True),
                ),
                (
                    "updated",
                    utils.fields.DateTimeWithoutTZField(auto_now=True, null=True),
                ),
            ],
            options={
                "db_table": "locale",
            },
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("PUBLIC", "Public"), ("PRIVATE", "Private")],
                        default="PUBLIC",
                        max_length=15,
                    ),
                ),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
                (
                    "name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="named_schools",
                        to="common.translation",
                    ),
                ),
            ],
            options={
                "db_table": "school",
            },
        ),
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("branch", models.CharField(max_length=64)),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="classes",
                        to="user.school",
                    ),
                ),
            ],
            options={
                "db_table": "class",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("restored_at", models.DateTimeField(blank=True, null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                ("phone_verified", models.BooleanField(default=False)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("email_verified", models.BooleanField(default=False)),
                ("fullname", models.CharField(blank=True, max_length=255)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("none", "None"),
                            ("student", "Student"),
                            ("teacher", "Teacher"),
                            ("staff", "Staff"),
                            ("editor", "Editor"),
                            ("admin", "Admin"),
                        ],
                        default="student",
                        max_length=64,
                    ),
                ),
                (
                    "creation_type",
                    models.CharField(
                        choices=[
                            ("PERSONAL", "Personal"),
                            ("BUSINESS", "Business"),
                            ("INTERNAL", "Internal"),
                        ],
                        max_length=16,
                    ),
                ),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
                (
                    "deleted_at",
                    utils.fields.DateTimeWithoutTZField(blank=True, null=True),
                ),
                (
                    "account",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "avatar",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="user.avatar",
                    ),
                ),
                (
                    "locale",
                    models.ForeignKey(
                        default=user.models.Locale.get_default_id,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="user.locale",
                    ),
                ),
                (
                    "school",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="users",
                        to="user.school",
                    ),
                ),
                (
                    "student_class",
                    models.ForeignKey(
                        db_column="class_id",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="users",
                        to="user.class",
                    ),
                ),
            ],
            options={
                "db_table": "user",
                "indexes": [
                    models.Index(fields=["created"], name="user_created_ff2248_idx")
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    ("deleted_at__isnull", True),
                    ("phone__isnull", False),
                    models.Q(("phone", ""), _negated=True),
                ),
                fields=("phone",),
                name="user_unique_phone",
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    ("deleted_at__isnull", True),
                    ("email__isnull", False),
                    models.Q(("email", ""), _negated=True),
                ),
                fields=("email",),
                name="user_unique_email",
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("email__isnull", False),
                        models.Q(("email__exact", ""), _negated=True),
                    ),
                    models.Q(
                        ("phone__isnull", False),
                        models.Q(("phone__exact", ""), _negated=True),
                    ),
                    _connector="OR",
                ),
                name="user_at_least_email_or_phone_not_null",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="class",
            unique_together={("branch", "school")},
        ),
    ]