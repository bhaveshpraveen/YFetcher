# Generated by Django 3.1.5 on 2021-01-23 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='publishing_datetime',
            new_name='published_at',
        ),
    ]