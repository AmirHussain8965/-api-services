from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import API
from accounts.models import PAYMENT

import time
from datetime import date

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode




# def paymentdouble(request):
#     final = True
#     paymentpurchased = PAYMENT.objects.filter(user=request.user, status="purchased")
#     paymentpaid = PAYMENT.objects.filter(user=request.user, status="paid")
#     if paymentpurchased.exists():
#         paypurobj = paymentpurchased.last()
#         if len(paymentpurchased) > 1:
#             for payments in paymentpurchased:
#                 paypurobj

        



def index(request):

    return render(request, "index.html")





@login_required(login_url='/signin/')
def pricing(request):
    paymentpurchased = PAYMENT.objects.filter(user=request.user, status="purchased")
    if paymentpurchased.exists():
        return render(request, "upgrade.html")
    context = {
        "stripe": settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, "pricing.html", context)



@login_required(login_url='/signin/')
def generateapi(request):
    api = API()
    payment = PAYMENT.objects.filter(user=request.user, status="paid")
    if payment.exists():
        tim = str(time.time()).split(".")[0]
        payment = payment.last()
        api.user = request.user
        api.key = urlsafe_base64_encode(force_bytes(tim))
        api.payment = payment
        api.save()
        payment.status = 'purchased'
        payment.save()
        return redirect("/setting/")
    return HttpResponseForbidden()







@login_required(login_url='/signin/')
def setting(request):
    payment = PAYMENT.objects.filter(user=request.user, status="purchased")
    if payment.exists():
        payment = payment.last()
        api = API.objects.filter(user=request.user, payment=payment).last()

        # Date Section
        
        olddate = api.created_at
        newdate = date.today()
        date1 = date(olddate.year, olddate.month, olddate.day)
        date2 = date(newdate.year, newdate.month, newdate.day)
        days_left = payment.sub_exp - (date2-date1).days
        context = {
            'api': api,
            "days_left": days_left if days_left > 0 else 0,
        }
        return render(request, "setting.html", context)
    return redirect('pricing')





def about(request):
    return render(request, "about.html")


def contact(request):
    context = {
        'black': True
    }
    return render(request, "contact.html", context)