# Generated by Django 4.2.11 on 2024-04-15 12:39

from django.db import migrations, models
import utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactVerification",
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
                    "medium",
                    models.CharField(
                        choices=[("email", "Email"), ("phone", "Phone")], max_length=64
                    ),
                ),
                ("receiver_address", models.CharField(max_length=1024)),
                ("code", models.CharField(max_length=6)),
                ("valid_interval_in_seconds", models.IntegerField(default=300)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("initial", "Initial"),
                            ("sent", "Sent"),
                            ("failed", "Failed"),
                            ("verified", "Verified"),
                        ],
                        default="initial",
                        max_length=64,
                    ),
                ),
                ("created", utils.fields.DateTimeWithoutTZField(auto_now_add=True)),
                ("updated", utils.fields.DateTimeWithoutTZField(auto_now=True)),
            ],
            options={
                "db_table": "contact_verification",
            },
        ),
        migrations.AddConstraint(
            model_name="contactverification",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    ("status", "initial"), ("status", "sent"), _connector="OR"
                ),
                fields=("code", "status"),
                name="unique_code_status_when_not_finished",
            ),
        ),
    ]
