from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .myforms import *
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import json
import requests

from Event_Management_System.celery import add
from api.tasks import sub


# Create your views here.
class WelcomePage(View):
    def get(self, req):
        events = get_public_events_list()
        context = {"events": events}
        return render(req, "WelcomePage.html", context=context)


def get_public_events_list():
    get_response = requests.get("http://127.0.0.1:8000/api/event/public-event-list/")
    json_data = json.loads(str(get_response.text))
    events = [e for e in json_data]
    return events


class UserRegistration(View):

    def get(self, req):
        form_obj = UserRegistrationForm()
        context = {"form_obj": form_obj}
        return render(req, "UserRegistrationForm.html", context=context)


class UserLogin(View):
    def get(self, req):
        data = req.GET
        if "requresting_url" in data:
            pass
        form_obj = UserLoginForm()
        context = {"form_obj": form_obj}
        return render(req, "UserLoginForm.html", context=context)


class UserLogout(View):
    def get(self, req):
        response = HttpResponse()
        response.delete_cookie("access", path="/")
        response.delete_cookie("refresh", path="/")
        return response


# Events
class CreateEvent(View):
    def get(self, req):
        form_obj = EventForm()
        context = {"form_obj": form_obj}
        return render(req, "EventCreateForm.html", context=context)


class EventDetail(View):
    def get(self, req, event_id):
        tokens = get_tokens(req)
        event = self.get_event_details(tokens, event_id)
        context = {"event": event}
        return render(req, "EventDetails.html", context=context)

    def get_event_details(self, tokens, event_id):
        access_token = tokens.get("access")
        header = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            f"http://127.0.0.1:8000/api/event/{event_id}/retrive/", headers=header
        )
        event = json.loads(str(response.text))
        return event


# User Dashboard
class UserDashboard(View):
    def get(self, req):
        print(req.headers)
        # cookie_dict = get_cookie_dict(req.headers["Cookie"])
        if not user_authenticate(req):
            print("Not authorized")
            return HttpResponseRedirect(reverse("user_login_page"))

        events = get_public_events_list()
        context = {"events": events}
        return render(req, "Dashboard.html", context=context)


class MyEventsView(View):
    def get(self, req):
        tokens = get_tokens(req)
        myevents = self.get_my_events(tokens)
        choices = get_event_choice_data(tokens)
        print(choices)
        form_obj = InviteSentForm()
        form_obj.fields.get("event_id").choices = choices
        # form_obj.events.choices = [('hi', 'Hi'), ('hello', 'Hello')]
        context = {"events": myevents, "form_obj": form_obj}
        return render(req, "MyEvent.html", context=context)

    def get_my_events(self, tokens):
        access_token = tokens.get("access")
        header = {"Authorization": f"Bearer {access_token}"}
        # print(header)
        response = requests.get(
            "http://127.0.0.1:8000/api/user/events-list/", headers=header
        )
        json_data = json.loads(str(response.text))
        myevents = [e for e in json_data]

        return myevents


class EventUpdateView(View):
    def get(self, req, event_id):
        curr_event = EventUpdateView.get_event_update_data(event_id)
        updateform = EventUpdateForm(initial=curr_event)
        context = {"form_obj": updateform}
        return render(req, "EventUpdateForm.html", context=context)

    def get_event_update_data(event_id):
        response = requests.get(f"http://127.0.0.1:8000/api/event/{event_id}/update/")
        curr_event = json.loads(str(response.text))
        curr_event["event_time"] = EventUpdateView.format_datetime(
            curr_event["event_time"]
        )
        return curr_event

    def format_datetime(time_s):
        return str(time_s[:10] + " " + time_s[11:16])


class InvitationsView(View):
    def get(self, req):
        tokens = get_tokens(req)
        choices = get_event_choice_data(tokens)

        invited_list = self.get_invited_list(tokens) 
        print(choices)
        form_obj = InviteSentForm()
        form_obj.fields.get("event_id").choices = choices
        context = {"form_obj": form_obj, "invites": invited_list}
        return render(req, "InvitationsBase.html", context=context)
    
    def get_invited_list(self, tokens):
        access_token = tokens.get("access")
        header = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(
            # reverse('invited_list'),
            "http://127.0.0.1:8000/api/invite/invited-list/",
            headers=header
        )
        # print(response.text)
        json_data = json.loads(str(response.text))
        return json_data


def get_event_choice_data(tokens):
    access_token = tokens.get("access")
    header = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "http://127.0.0.1:8000/api/event/event-choices/", headers=header
    )
    json_data = json.loads(str(response.text))
    print(json_data)
    choices = [(c["event_id"], c["title"]) for c in json_data]
    return choices


def get_tokens(req):
    cookie_dict = get_cookie_dict(req.headers["Cookie"])

    if (not ("access" in cookie_dict)) or (not ("refresh" in cookie_dict)):
        raise Exception("Token not present!")

    return {"access": cookie_dict["access"], "refresh": cookie_dict["refresh"]}


def user_authenticate(req) -> bool:
    if not ("Cookie" in req.headers) and not ("access" in req.headers):
        return False
    cookie_dict = get_cookie_dict(req.headers["Cookie"])
    print("Cookie dict", cookie_dict)

    if (not ("access" in cookie_dict)) or (not ("refresh" in cookie_dict)):
        return get_new_token_pair()

    body = {"token": cookie_dict["access"]}
    response = requests.post("http://127.0.0.1:8000/api/user/verifytoken/", data=body)
    print(response.text)

    if response.ok:
        return True

    # Call to get refreshed token
    return get_refreshed_token(cookie_dict)


def get_refreshed_token(cookie_dict):
    body = {"refresh": cookie_dict["refresh"]}
    response = requests.post(
        "http://127.0.0.1:8000/api/user/refreshed-token/", data=body
    )

    if response.ok:
        return True

    return get_new_token_pair()


def get_new_token_pair():
    # return HttpResponseRedirect(reverse('user_login_page'))
    return False


def get_cookie_dict(s: str):
    cookie_dict = {}
    lst = s.split(";")

    for e in lst:
        x = e.strip()
        key, value = tuple(x.split("="))
        cookie_dict[key] = value

    return cookie_dict
