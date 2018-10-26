from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.


def index(request):
    return render(request,"index.html")


def login(request):
    return render(request,"login.html")


def account(request):
    return render(request,"account.html")