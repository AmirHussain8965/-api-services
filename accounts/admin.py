from django.contrib import admin
from .models import *


class SUBSCRIPTIONAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'calls', 'days')



class PAYMENTAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'sub_id', 'sub_name', 'sub_price', 'sub_date', 'sub_exp')
    list_filter = ['status']


admin.site.register(SUBSCRIPTION, SUBSCRIPTIONAdmin)
admin.site.register(PAYMENT, PAYMENTAdmin)