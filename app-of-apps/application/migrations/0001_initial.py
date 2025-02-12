# Generated by Django 5.1.6 on 2025-02-12 20:38

import application.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Applications",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "API_KEY",
                    models.CharField(
                        default=application.models.generate_api_key,
                        editable=False,
                        max_length=255,
                        unique=True,
                    ),
                ),
                ("created_ts", models.DateTimeField(auto_now_add=True)),
                ("updated_ts", models.DateTimeField(auto_now=True)),
                ("deleted_ts", models.DateTimeField(blank=True)),
            ],
        ),
    ]
