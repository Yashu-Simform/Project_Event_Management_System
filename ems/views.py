from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .myforms import *

import requests

# Create your views here.
class WelcomePage(View):
    def get(self, req):
        get_response = requests.get('http://127.0.0.1:8000/api/event/public-event-list/')
        print(get_response.text)
        # context = {'events': events}
        return render(req, 'WelcomePage.html')
    
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

