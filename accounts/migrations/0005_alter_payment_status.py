# Generated by Django 4.0.4 on 2022-05-26 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_payment_sub_calls_alter_payment_sub_exp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('create', 'create'), ('paid', 'paid'), ('purchased', 'purchased'), ('done', 'done')], default='create', max_length=200),
        ),
    ]
