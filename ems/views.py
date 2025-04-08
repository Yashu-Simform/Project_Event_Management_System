from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .myforms import *
import json

import requests

# Create your views here.
class WelcomePage(View):
    def get(self, req):
        events = get_public_events_list()
        context = {'events': events}
        return render(req, 'WelcomePage.html', context=context)
    

def get_public_events_list():
    get_response = requests.get('http://127.0.0.1:8000/api/event/public-event-list/')
    json_data = json.loads(str(get_response.text))
    events = [e for e in json_data]
    return events

class UserRegistration(View):

    def get(self, req):
        form_obj = UserRegistrationForm()
        context = {'form_obj': form_obj}
        return render(req, 'UserBaseForm.html', context=context)

    # def post(self, req):
    #     form_obj = UserRegistration(req.POST)

class UserLogin(View):
    def get(self, req):
        form_obj = UserLoginForm()
        context = {'form_obj': form_obj}
        return render(req, 'UserLoginForm.html', context=context)


# Events
class CreateEvent(View):
    def get(self, req):
        form_obj = EventForm()
        context = {'form_obj': form_obj}
        return render(req, 'EventCreateForm.html', context=context)
    

# User Dashboard
class UserDashboard(View):
    def get(self, req):
        events = get_public_events_list()
        context = {'events': events}
        return render(req, 'Dashboard.html', context=context)