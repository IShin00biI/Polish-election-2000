from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    if (request.user.is_authenticated):
        return HttpResponse("Hi, %s!" % request.user.username)
    else:
        return HttpResponse("Hi, nobody!")