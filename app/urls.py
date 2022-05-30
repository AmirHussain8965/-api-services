
from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name="index"),
    path('pricing/', pricing, name="pricing"),
    path('generateapi/', generateapi, name="generateapi"),
    path('setting/', setting, name="setting"),



    # Nav bar Urls
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
]
