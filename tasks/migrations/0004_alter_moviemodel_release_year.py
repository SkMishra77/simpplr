# Generated by Django 5.0.6 on 2024-06-19 18:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_moviemodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviemodel',
            name='release_year',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
