# Generated by Django 5.1.1 on 2024-10-15 04:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("help_desk", "0002_remove_ticket_assign_to_ticketassignment_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticketassignment",
            name="message",
            field=models.TextField(blank=True, null=True),
        ),
    ]
