from django import template
register = template.Library()
from accounts.models import PAYMENT
from django.contrib.auth.models import User

@register.simple_tag
def checkpayment(id): # Only one argument.
    user = User.objects.filter(id=id).last()
    payment = PAYMENT.objects.filter(user=user, status="purchased")
    paymentpaid = PAYMENT.objects.filter(user=user, status="paid")
    if payment.exists():
        return "true"
    if paymentpaid.exists():
        return "true1"
    
    
    return False



# register.filter('checkpayment', checkpayment)