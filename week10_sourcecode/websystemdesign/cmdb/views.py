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


def regist_succusess(request):
    return render(request,"regist_succusess.html")



def logout(request):
    return render(request,"logout.html")

@login_required(login_url='login.html')
def account(request):
    post_list = Post.objects.filter(author = request.user.username)
    return render(request,"account.html",{'post_list': post_list,'username': request.user.username})


def uploadImg(request): # 图片上传函数
    if request.method == 'POST':
        new_img = Post(
                name=request.POST.get('keyword'),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                zipcode=request.POST.get('zipcode'),
                author=request.user.username,
                img_url=request.FILES.get('img'),
                categories=request.POST.get('categories')
            )
        new_img.save()
    return render(request, 'imgUpload.html')


def showImg(request):
    post_list = Post.objects.all()  # 查询所有的信息
    return render(request, "showImg.html", {'post_list': post_list})


def category(request):
    post_list = Post.objects.all()  # 查询所有的信息
    return render(request,"category.html", {'post_list': post_list})


def animals(request):
    post_list = Post.objects.filter(categories__contains="Animal")  # 查询所有的信息
    return render(request,"animals.html", {'post_list': post_list})


def architecture(request):
    post_list = Post.objects.filter(categories__contains="Architecture")
    return render(request,"Architecture.html", {'post_list': post_list})


def food(request):
    post_list = Post.objects.filter(categories__contains="Food")
    return render(request,"Food.html", {'post_list': post_list})


def landscapes(request):
    post_list = Post.objects.filter(categories__contains="Landscape")  # 查询所有的信息
    return render(request,"Landscapes.html", {'post_list': post_list})


def portrait(request):
    post_list = Post.objects.filter(categories__contains="Portrait")  # 查询所有的信息
    return render(request,"Portrait.html", {'post_list': post_list})


def other(request):
    post_list = Post.objects.filter(categories__contains="Other")  # 查询所有的信息
    return render(request,"Other.html", {'post_list': post_list})


def search(request):
    q = request.GET.get('q')
    error_msg="error!!!!!"
    post_list = Post.objects.filter(name__icontains=q)
    print(post_list)
    return render(request, 'result.html', {'error_msg': error_msg,
                                               'post_list': post_list})

def result(request):
    return render(request,"result.html")

# Create your views here.

def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']


            # 判断用户是否存在
            user = auth.authenticate(username = username,password = password)
            if user:
                context['userExit']=True
                return render(req, 'login.html', context)


            #添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username=username, password=password)
            user.save()

            #添加到session
            req.session['username'] = username
            #调用auth登录
            auth.login(req, user)
            #重定向到首页
            return render(req,'regist_succusess.html')
    else:
        context = {'isLogin':False}
    #将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return  render(req,'register.html',context)

#登陆

def login_view(req):
    context = {}
    print("@@@@@@@@@@@@@@")
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获取表单用户密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #获取的表单数据与数据库进行比较
            re = authenticate(username = username,password = password)
            if re:
                #比较成功，跳转index
                auth.login(req,re)
                req.session['username'] = username
                return render(req,'account.html')
            else:
                print("@@@@@@@@@@@@@@")
                #比较失败，还在login
                context = {'isLogin': False,'pawd':False}
                return render(req, 'index.html', context)

    return render(req, 'login.html')

#登出
def logout_view(req):
    #清理cookie里保存username
    auth.logout(req)
    return render(req, 'logout.html')


def viewimge(request):
    p1 = request.GET.get('p1')
    p2 = request.GET.get('p2')
    p3 = request.GET.get('p3')
    p4 = request.GET.get('p4')
    p5 = request.GET.get('p5')
    p6 = request.GET.get('p6')
    p7 = request.GET.get('p7')
    p8 = request.GET.get('p8')

    context = {'img_url': p2,
               'img_keyword': p1,
               'img_author': p3,
               'img_address': p4,
               'img_categories': p5,
               'img_city': p6,
               'img_zipcode': p7,
               'img_state': p8,


               }

    print(context['img_url'])
    return render(request, 'viewimge.html',context)