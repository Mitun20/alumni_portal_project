# Generated by Django 5.1.1 on 2024-10-09 10:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("account", "0008_alter_alumni_linked_in_alter_alumni_website"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TicketCategory",
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
                ("category", models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name="TicketStatus",
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
                ("status", models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
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
                (
                    "priority",
                    models.CharField(
                        choices=[("L", "Low"), ("M", "Medium"), ("H", "High")],
                        max_length=225,
                    ),
                ),
                ("due_date", models.DateField(blank=True, null=True)),
                ("last_status_on", models.DateField(auto_now=True)),
                ("content", models.TextField()),
                (
                    "alumni",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="account.alumni"
                    ),
                ),
                (
                    "assign_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="help_desk.ticketcategory",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="help_desk.ticketstatus",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TicketAssignment",
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
                ("response", models.TextField(blank=True, null=True)),
                ("assigned_on", models.DateField(auto_now_add=True)),
                ("respond_on", models.DateField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned_tickets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="help_desk.ticket",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TicketReply",
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
                ("message", models.TextField()),
                ("posted_on", models.DateField(auto_now_add=True)),
                (
                    "posted_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="help_desk.ticket",
                    ),
                ),
            ],
        ),
    ]
