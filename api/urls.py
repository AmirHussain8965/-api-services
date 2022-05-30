
from django.urls import path
from .views import *


urlpatterns = [
    path('getApi/<slug:api_key>/', getdate, name="index"),
]
