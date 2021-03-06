# Generated by Django 3.1.5 on 2021-01-23 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feed", "0002_auto_20210123_1726"),
    ]

    operations = [
        migrations.RenameField(
            model_name="video",
            old_name="etag",
            new_name="unique_video_id",
        ),
        migrations.AlterField(
            model_name="video",
            name="published_at",
            field=models.DateTimeField(
                db_index=True, null=True, verbose_name="Video Published At"
            ),
        ),
    ]
