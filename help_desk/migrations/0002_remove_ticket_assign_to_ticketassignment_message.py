# Generated by Django 5.1.1 on 2024-10-14 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("help_desk", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="assign_to",
        ),
        migrations.AddField(
            model_name="ticketassignment",
            name="message",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
