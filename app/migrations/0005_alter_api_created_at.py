# Generated by Django 4.0.4 on 2022-05-26 11:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_api_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]