# Generated by Django 4.0.4 on 2022-05-26 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='api',
            name='call',
        ),
    ]
