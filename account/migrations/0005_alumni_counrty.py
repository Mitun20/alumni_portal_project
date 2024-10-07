# Generated by Django 5.1.1 on 2024-10-07 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0004_remove_member_department_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="alumni",
            name="counrty",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="account.country",
            ),
        ),
    ]
