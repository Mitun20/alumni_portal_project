# Generated by Django 5.1.1 on 2024-10-09 04:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("job_portal", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="job_post",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="job_portal.jobpost",
            ),
            preserve_default=False,
        ),
    ]
