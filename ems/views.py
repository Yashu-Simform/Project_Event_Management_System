from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class WelcomePage(View):
    def get(self, req):
        return HttpResponse('<h1>Welcome!</h1>')