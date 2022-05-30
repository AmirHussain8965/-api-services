from django.contrib import admin
from .models import API



class APIAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'payment')



admin.site.register(API, APIAdmin)