# Generated by Django 5.1.1 on 2024-10-07 11:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_alumni_counrty"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="alumni",
            name="counrty",
        ),
    ]
