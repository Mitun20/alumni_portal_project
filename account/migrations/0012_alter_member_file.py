# Generated by Django 5.1.2 on 2024-11-19 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_member_department_member_file_member_is_approve_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='proofs/'),
        ),
    ]