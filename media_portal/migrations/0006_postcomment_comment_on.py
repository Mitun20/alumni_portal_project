# Generated by Django 5.1.2 on 2024-11-26 07:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("media_portal", "0005_alter_post_blog_alter_post_content_alter_post_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="postcomment",
            name="comment_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]