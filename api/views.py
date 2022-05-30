from django.http.response import HttpResponse
from app.models import API


from datetime import date

import json

def getdate(request, api_key):
    api = API.objects.filter(key=api_key)
    if api.exists():
        api = api.first()
        api_call = api.payment.sub_calls
        olddate = api.created_at
        newdate = date.today()
        date1 = date(olddate.year, olddate.month, olddate.day)
        date2 = date(newdate.year, newdate.month, newdate.day)
        daysLeft = api.payment.sub_exp - (date2-date1).days
        if api_call > 0 and daysLeft > 0:
            api_call = api_call - 1
            dictionory = {
                'api_key': api_key,
                "status": "success",
                'daysLetf': daysLeft,
                "apiCallLeft": api_call,
                "message": f"Hi there, your api key is valid for {daysLeft} days. You have {api_call} api calls left.",
            }
            api.payment.sub_calls = api_call
            api.payment.save()
            api.save()
            dictionory = json.dumps(dictionory)
            response = HttpResponse(dictionory)
            response['Content-Type'] = 'application/json'
            return response
        else:
            if api_call <= 0:
                dictionory = {
                    'api_key': api_key,
                    "status": "error",
                    "message": "You have no api calls left.",
                    "website": "https://apiservices.com/",
                }
            elif daysLeft <= 0:
                dictionory = {
                    'api_key': api_key,
                    "status": "error",
                    "message": f"Your time limit for the api call is over.",
                    "website": "https://apiservices.com/",
                }
                
            dictionory = json.dumps(dictionory)
            response = HttpResponse(dictionory)
            response['Content-Type'] = 'application/json'
            return response
        
        

    else:
        dictionory = json.dumps({"status": "error", "message": "Invalid API Key"})
        response = HttpResponse(dictionory)
        response['Content-Type'] = 'application/json'
        return response




