from django.urls import path
from .views import *


urlpatterns = [

    # Account Urls
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('logout/', logoutview,name='logout'),




    # Reset Urls
    path('forget/', forget),
	path('reset-password/<username>/', reset_user, name="reset-password"),
	path('new-password/', new_password),


    # Activate Urls
	path('account-activation/<username>/', activate_user, name="account-activation"),





    # Payment Urls
    path("payment/<int:id>/", create_checkout_session, name='api_checkout_session'),
]