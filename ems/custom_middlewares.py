import requests
from django.http import HttpResponseRedirect
from django.urls import reverse


def auth_required():
    def wrapper(req, *args, **kwargs):
        pass


def user_authenticate(cookie_dict):
    print("Cookie dict", cookie_dict)
    body = {"token": cookie_dict["access"]}
    response = requests.post("http://127.0.0.1:8000/api/user/verifytoken/", data=body)
    print(response.text)

    # Call to get refreshed token
    if not response.ok:
        return get_refreshed_token()

    return True


def get_refreshed_token(cookie_dict):
    body = {"refresh": cookie_dict["refresh"]}
    response = requests.post(
        "http://127.0.0.1:8000/api/user/refreshed-token/", data=body
    )

    if not response.ok:
        return get_new_token_pair()


def get_new_token_pair():
    return HttpResponseRedirect(reverse("user_login_page"))


def get_cookie_dict(s: str):
    cookie_dict = {}
    lst = s.split(";")

    for e in lst:
        x = e.strip()
        key, value = tuple(x.split("="))
        cookie_dict[key] = value

    return cookie_dict
