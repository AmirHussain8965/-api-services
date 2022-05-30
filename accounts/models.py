from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now




class SUBSCRIPTION(models.Model):
    name = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=10000000, decimal_places=2)
    calls = models.IntegerField()
    days = models.IntegerField()
    def __str__(self):
        return self.name



class PAYMENT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=200)
    session_id = models.CharField(max_length=254, null=True, blank=True)
    STATUS_OPTION = [
        ('create', 'create'),
        ('paid', 'paid'),
        ('purchased', 'purchased'),
        ('done', 'done'),
    ]
    status = models.CharField(max_length=200, default='create', choices=STATUS_OPTION)
    sub_id = models.CharField(max_length=200)
    sub_name = models.CharField(max_length=200, null=True, blank=True)
    sub_price = models.CharField(max_length=200, null=True, blank=True)
    sub_date = models.DateTimeField(default=now)
    sub_calls = models.IntegerField(null=True, blank=True)
    sub_exp = models.IntegerField(default=30, null=True, blank=True)
    def __str__(self):
        return self.user.username


