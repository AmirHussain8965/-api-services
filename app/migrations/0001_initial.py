# Generated by Django 4.0.4 on 2022-05-26 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_rename_date_payment_sub_date_payment_sub_exp_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='API',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('call', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
