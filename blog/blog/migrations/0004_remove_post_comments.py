# Generated by Django 3.2.16 on 2023-11-06 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
    ]
