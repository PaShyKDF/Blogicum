# Generated by Django 3.2.16 on 2023-11-06 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.comments', verbose_name='Комментарии'),
        ),
    ]