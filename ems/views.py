from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .myforms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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
        data = req.GET
        if 'requresting_url' in data:
            pass
        form_obj = UserLoginForm()
        context = {'form_obj': form_obj}
        return render(req, 'UserLoginForm.html', context=context)
    
class UserLogout(View):
    def get(self, req):
        response = HttpResponse()
        response.delete_cookie('access',path='/')
        response.delete_cookie('refresh', path='/')
        return response


# Events
class CreateEvent(View):
    def get(self, req):
        form_obj = EventForm()
        context = {'form_obj': form_obj}
        return render(req, 'EventCreateForm.html', context=context)
    

# User Dashboard
class UserDashboard(View):
    def get(self, req):
        print(req.headers)
        cookie_dict = get_cookie_dict(req.headers['Cookie'])
        if not user_authenticate(cookie_dict):
            print('Not authorized')
            return HttpResponseRedirect(reverse('user_login_page'))
            
        events = get_public_events_list()
        context = {'events': events}
        return render(req, 'Dashboard.html', context=context)
    

class MyEventsView(View):
    def get(self, req):
        tokens = get_tokens(req)
        myevents = self.get_my_events(tokens)
        context = {'events': myevents}
        return render(req, 'MyEvent.html', context=context)

    def get_my_events(self, tokens):
        access_token = tokens.get('access')
        header = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('http://127.0.0.1:8000/api/user/events-list/', headers=header) 
        json_data = json.loads(str(response.text))
        myevents = [e for e in json_data]

        return myevents
    
def get_tokens(req):
    cookie_dict = get_cookie_dict(req.headers['Cookie'])

    if (not ('access' in cookie_dict)) or (not ('refresh' in cookie_dict)):
        raise Exception('Token not present!')

    return {'access': cookie_dict['access'], 'refresh': cookie_dict['refresh']}

def user_authenticate(cookie_dict) -> bool:
    print('Cookie dict', cookie_dict)

    if (not ('access' in cookie_dict)) or (not ('refresh' in cookie_dict)): 
        return get_new_token_pair()

    body = {'token': cookie_dict['access']}
    response = requests.post('http://127.0.0.1:8000/api/user/verifytoken/', data=body)
    print(response.text)


    if response.ok:
        return True

    # Call to get refreshed token
    return get_refreshed_token()

    
def get_refreshed_token(cookie_dict):
    body = {'refresh': cookie_dict['refresh']}
    response = requests.post('http://127.0.0.1:8000/api/user/refreshed-token/', data=body)
    
    if response.ok:
        return True

    return get_new_token_pair()

def get_new_token_pair():
    # return HttpResponseRedirect(reverse('user_login_page'))
    return False


def get_cookie_dict(s: str):
    cookie_dict = {}
    lst = s.split(';')

    for e in lst:
        x = e.strip()
        key, value = tuple(x.split('='))
        cookie_dict[key] = value

    return cookie_dict