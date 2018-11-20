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



def get_data(request):#获取数据库的数据
    post_list = Post.objects.all()  # 从数据库中取出所有的图片路径
    return render(request, 'showImg.html', {'post_list': post_list})


def search(request):
    q = request.GET.get('q')
    error_msg="error!!!!!"
    post_list = Post.objects.filter(name__icontains=q)
    print(post_list)
    return render(request, 'result.html', {'error_msg': error_msg,
                                               'post_list': post_list})

def result(request):
    return render(request,"result.html")


