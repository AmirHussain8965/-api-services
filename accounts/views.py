from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseForbidden
import hashlib
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode



import stripe
from .models import PAYMENT, SUBSCRIPTION
from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


@login_required(login_url='/signin/', redirect_field_name=None)
def logoutview(request):
	logout(request)
	messages.add_message(request, messages.ERROR, 'Logout Successfully')
	return redirect('/signin/')


@csrf_exempt
def signin(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				print(request.GET)
				if 'next' in request.GET:
					return redirect(request.GET.get('next'))
				else:
					return redirect('/')
			else:
				messages.add_message(request, messages.ERROR, mark_safe('Your Account Is Not Verified, Please Check Your &nbsp<a class="btn btn-outline-warning" href="https://gmail.com" target="_blanck">Gmail</a> Inbox Or Spam'))
				send_activation_email(user, request)
		else:
			messages.add_message(request, messages.ERROR, 'Invalid Credentials')
	return render(request, 'account/signin.html', {"app_path": request.get_full_path()})












def send_activation_email(user, request):
	current_site = get_current_site(request)
	email_subject = "Activate Your Account"
	email_body = render_to_string('mail/activation.html', {
		"domain":current_site,
		"username": urlsafe_base64_encode(force_bytes(user.username)),
	})
	email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, 
	to=[user.email])
	email.send()


def activate_user(request, username):
	try:
		email = force_str(urlsafe_base64_decode(username))
		user = User.objects.filter(username=email).first()
    
	except:
		user = None
	
	if user != None:
		user.is_active = True
		user.save()
		messages.add_message(request, messages.ERROR, 'Your Account Successfully Activated')
		return redirect('/signin/')
	return HttpResponse('Failed')







@csrf_exempt
@csrf_protect
def signup(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		pass1 = request.POST.get('password')
		if User.objects.filter(username=email).exists():
			messages.add_message(request, messages.ERROR, mark_safe('Email Already Exists, Please Try To &nbsp<a class="btn btn-outline-warning" href="/signin/">Signin</a>'))
		else:
			user = User.objects.create_user(username=email, email=email, password=pass1)
			user.is_active = False
			user.save()
			send_activation_email(user, request)
			messages.add_message(request, messages.ERROR, mark_safe('Your Account Is Created To Verify, Please Check Your &nbsp<a class="btn btn-outline-warning" href="https://gmail.com" target="_blanck">Gmail</a> Inbox Or Spam'))
	return render(request, 'account/signup.html')







def hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


def send_forget_email(user, request):
	current_site = get_current_site(request)
	email_subject = "Reset Your Account Password"
	email_body = render_to_string('mail/reset.html', {
		"domain":current_site,
		"username": urlsafe_base64_encode(force_bytes(user.username)),
	})
	email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, 
	to=[user.email])
	email.send()


def reset_user(request, username):
    try:
        email = force_str(urlsafe_base64_decode(username))
        user = User.objects.filter(username=email).first()
    
    except Exception as e:
        user = None

    if user != None:
        return render(request, 'account/newpassword.html', {"user":user.username})
    return HttpResponse('Failed')




@csrf_protect
@csrf_exempt
def forget(request):
	if request.method=='POST':
		email = request.POST.get('email')
		if User.objects.filter(email=email).exists():
			user = User.objects.filter(email=email).first()
			send_forget_email(user, request)
			messages.add_message(request, messages.ERROR, 'Password Reset Email Send To Your Gmail, Please Check Inbox And Spam!')
			return render(request, 'account/forget.html')
		else:
			messages.add_message(request, messages.ERROR, 'Email Does not Exist!')
	return render(request, 'account/forget.html')



@csrf_protect
@csrf_exempt
def new_password(request):
	if request.method == 'POST':
		newpass = request.POST.get('password')
		email = request.POST.get('user')
		user = User.objects.filter(username=email).first()
		user.set_password(str(newpass))
		user.save()
		messages.add_message(request, messages.ERROR, 'Password Reset Successfully')
		return redirect('/signin/')
	return HttpResponseForbidden()






















####################################
##########----- Payment ---#########
####################################





def paypalpaymentsuccess(request, id):
	return render(request, "payments/paymentsuccess.html", {"prodid": id})


@csrf_exempt
def create_checkout_session(request, id):
	id = int(id)
	stripe.api_key = settings.STRIPE_TEST_KEY
	sub = SUBSCRIPTION.objects.filter(id=1).first()
	checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'], 
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': 'Package',
                    },
                    'unit_amount': id * 100,
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + f"?prodid={1}" + "&session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('failed')),
    )
	
	order = PAYMENT()
	user_obj = User.objects.filter(username=request.user.username).first()
	order.user = user_obj
	order.sub_id = sub.id
	order.status = 'create'
	order.stripe_payment_intent = checkout_session['payment_intent']
	order.save()
	return JsonResponse({'sessionId': checkout_session.id})






"""
.filter(session_id=session_id, status='done').filter(session_id=session_id, status='purchased')
"""

class PaymentSuccessView(TemplateView):
	template_name = "account/paymentsuccess.html"
	
	def get(self, request, *args, **kwargs):
		session_id = request.GET.get('session_id')
		prodid = request.GET.get('prodid')
		prodid = int(prodid)
		sub = SUBSCRIPTION.objects.filter(id=int(prodid))
		if session_id is None or PAYMENT.objects.filter(session_id=session_id, status='paid').exists() or not sub.exists():
			return HttpResponseNotFound()

		stripe.api_key = settings.STRIPE_TEST_KEY
		try:
			session = stripe.checkout.Session.retrieve(session_id)
		except:
			return HttpResponseNotFound()
		order = get_object_or_404(PAYMENT, stripe_payment_intent=session.payment_intent)
		sub = sub.first()
		if sub.id == int(order.sub_id):
			order.status = 'paid'
			order.prodid = prodid
			order.session_id = session_id
			order.sub_name = sub.name
			order.sub_price = sub.price
			order.sub_calls = sub.calls
			order.sub_exp = sub.days
			order.save()
			return render(request, self.template_name, {"prodid": prodid})
		else:
			return redirect("failed")



class PaymentFailedView(TemplateView):
    template_name = "account/paymentfailed.html"
