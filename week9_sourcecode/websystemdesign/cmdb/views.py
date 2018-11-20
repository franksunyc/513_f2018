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

class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密_码',widget=forms.PasswordInput())


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
                name=request.POST.get('name'),
                address=request.POST.get('address'),
                author=request.user.username,
                img_url=request.FILES.get('img'),
                categories=request.POST.get('categories')
            )
        new_img.save()
    return render(request, 'imgUpload.html')


def showImg(request):

    return render(request, 'showImg.html')


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

def text(request):
    return render(request,"text.html")




# Create your views here.

# 查下store全部信息
def select_store_list(request):
    store_list = Post.objects.all() #查询所有的信息
    print(type(store_list), store_list)  #打印结果类型与结果值
    return render(request, "store_list.html", {"content": store_list}) #返回界面


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
    return render(req, 'index.html')
