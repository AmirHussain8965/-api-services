from django.db import models
from django.contrib.auth.models import User
from accounts.models import PAYMENT
from django.utils.timezone import now


class API(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)
    payment = models.ForeignKey(PAYMENT, on_delete=models.CASCADE)