# Generated by Django 5.1.1 on 2024-10-14 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0009_alter_member_skills_member"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alumni",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="alumni",
                to="account.member",
            ),
        ),
        migrations.AlterField(
            model_name="member_education",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="education",
                to="account.member",
            ),
        ),
        migrations.AlterField(
            model_name="member_experience",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="experience",
                to="account.member",
            ),
        ),
    ]
