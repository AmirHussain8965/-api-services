# Generated by Django 4.0.4 on 2022-05-26 11:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_payment_sub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='sub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
