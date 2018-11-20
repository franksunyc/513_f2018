from django.shortcuts import render,redirect, reverse
from django.shortcuts import HttpResponse,Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
from cmdb.models import Post

import MySQLdb

from django import forms    #导入表单
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from cmdb.forms import UserForm


def index(request):
    return render(request,"index.html")

def index(request):
    return render(request,"index.html")

def account(request):
    
    return render(request,"account.html",)
