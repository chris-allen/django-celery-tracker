# Generated by Django 4.1.1 on 2023-07-17 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_celery_tracker", "0002_celerytask_args"),
    ]

    operations = [
        migrations.AlterField(
            model_name="celerytask",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
