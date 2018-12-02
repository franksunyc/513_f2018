from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
from cmdb.models import Post
import operator
from functools import reduce
from uszipcode import SearchEngine
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from cmdb.forms import UserForm
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        return super().default(obj)






class User(object):
    def __init__(self, name):
        self.name = name


class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.name
        return json.JSONEncoder.default(self, obj)


def index(request):
    return render(request,"index.html")


def advancedsearch(request):
    if request.method == 'POST':
        query_type=request.POST.get('search_type')
        query_list = []
        distant_query_list=[]
        if query_type=="reguler":

            author_name=request.POST.get('uplader')
            zipcode_name=request.POST.get('zip')
            your_zipcode_name=request.POST.get('yourzip')
            distance_name=request.POST.get('distance')
            city_name=request.POST.get('city')
            state_name=request.POST.get('state')
            category_name=request.POST.get('sel1')
            keyword = request.POST.get('query')

            if len(keyword)!=0:
                keyword_query=Q(name__icontains=keyword)
                query_list.append(keyword_query)
            if len(author_name) != 0:
                author_query = Q(author=author_name)
                query_list.append(author_query)
            if len(zipcode_name) != 0:
                zipcode_query=Q(zipcode=zipcode_name)
                query_list.append(zipcode_query)
            if len(city_name)!=0:
                city_query = Q(city=city_name)
                query_list.append(city_query)
            if len(state_name)!=0:
                state_query=Q(state=state_name)
                query_list.append(state_query)
            if len(category_name)!= 0:
                print(category_name)
                if category_name=="All":

                    pass
                else:
                    category_query = Q(categories=category_name)
                    query_list.append(category_query)
            if len(your_zipcode_name) != 0 and len(distance_name) != 0:
                search = SearchEngine(simple_zipcode=True)
                zipcode_search = search.by_zipcode(int(your_zipcode_name))
                # zipcode = search.by_zipcode("01854", radius=30, returns=5)
                lat = zipcode_search.lat
                lng = zipcode_search.lng
                zipcode_search = search.by_coordinates(lat, lng, radius=int(distance_name), returns=100)
                for each in zipcode_search:
                    your_zip_code_query=Q(zipcode=each.zipcode)
                    distant_query_list.append(your_zip_code_query)
                if len(query_list)==0:
                    post_list = Post.objects.all().filter(reduce(operator.or_, distant_query_list))
                else:
                    post_list = Post.objects.all().filter(reduce(operator.and_, query_list),
                                                      reduce(operator.or_, distant_query_list))
                return render(request, 'result.html', {'post_list': post_list})
            post_list = Post.objects.all().filter(reduce(operator.and_, query_list))
            return render(request, 'result.html', {'post_list': post_list})
        if query_type == "location":
            city_name = request.POST.get('city')
            state_name = request.POST.get('state')
            zipcode_name = request.POST.get('zip')
            keyword = request.POST.get('query')
            if len(keyword) != 0:
                keyword_query = Q(name__icontains=keyword)
                query_list.append(keyword_query)
            if len(zipcode_name) != 0:
                zipcode_query=Q(zipcode=zipcode_name)
                query_list.append(zipcode_query)
            if len(city_name)!=0:
                city_query = Q(city=city_name)
                query_list.append(city_query)
            if len(state_name)!=0:
                state_query=Q(state=state_name)
                query_list.append(state_query)
            post_list = Post.objects.all().filter(reduce(operator.and_, query_list))
            return render(request, 'result.html', {'post_list': post_list})
        if query_type == "uploader":
            author_name = request.POST.get('uplader')
            keyword = request.POST.get('query')
            if len(keyword) != 0:
                keyword_query = Q(name__icontains=keyword)
                query_list.append(keyword_query)
            if len(author_name) != 0:
                author_query = Q(author=author_name)
                query_list.append(author_query)
                post_list = Post.objects.all().filter(reduce(operator.and_, query_list))
            return render(request, 'result.html', {'post_list': post_list})
        if query_type == "categories":
            category_name = request.POST.get('sel1')
            keyword = request.POST.get('query')
            if len(keyword) != 0:
                keyword_query = Q(name__icontains=keyword)
                query_list.append(keyword_query)
            if len(category_name)!= 0:
                print(category_name)
                if category_name=="All":
                    pass
                else:
                    category_query = Q(categories=category_name)
                    query_list.append(category_query)
                post_list = Post.objects.all().filter(reduce(operator.and_, query_list))
            return render(request, 'result.html', {'post_list': post_list})
        if query_type == "distance":
            print("##########")
            your_zipcode_name = request.POST.get('yourzip')
            keyword = request.POST.get('query')
            distance_name = request.POST.get('distance')
            if len(keyword) != 0:
                keyword_query = Q(name__icontains=keyword)
                query_list.append(keyword_query)
            if len(your_zipcode_name) != 0 and len(distance_name) != 0:
                search = SearchEngine(simple_zipcode=True)
                zipcode_search = search.by_zipcode(int(your_zipcode_name))
                print(zipcode_search)
                # zipcode = search.by_zipcode("01854", radius=30, returns=5)
                lat = zipcode_search.lat
                lng = zipcode_search.lng
                zipcode_search = search.by_coordinates(lat, lng, radius=int(distance_name), returns=100)
                for each in zipcode_search:
                    your_zip_code_query=Q(zipcode=each.zipcode)
                    query_list.append(your_zip_code_query)
                post_list = Post.objects.all().filter(reduce(operator.or_, query_list))
                return render(request, 'result.html', {'post_list': post_list})
    return render(request, "advancedsearch.html")
'''
query_list=[Q(zipcode='01854'),Q(zipcode='01852')]
    post_list = Post.objects.all().filter( reduce(operator.or_, query_list), Q(name__icontains=q) )


    return render(request, 'result.html', {'error_msg': error_msg,
                                               'post_list': post_list})

def adsearch(request):
    if request.method == 'POST':
        if request.POST.get('location'):
            print("ajajajajajajaj")
    
        name=request.POST.get('keyword'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        state=request.POST.get('state'),
        zipcode=request.POST.get('zipcode'),
        author=request.user.username,
        img_url=request.FILES.get('img'),
        categories=request.POST.get('categories')
            )
    q = request.GET.get('q')
    error_msg="error!!!!!"
    query_list=[Q(zipcode='01854'),Q(zipcode='01852')]
    post_list = Post.objects.all().filter( reduce(operator.or_, query_list), Q(name__icontains=q) )


    return render(request, 'result.html', {'error_msg': error_msg,
                                          'post_list': post_list})
'''
def regist_succusess(request):
    return render(request,"regist_succusess.html")



def logout(request):
    return render(request,"logout.html")

def map(request):
    return render(request,"map.html")

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

    line_list=[]
    post_list = Post.objects.all().filter( name__icontains=q)
    for each in post_list:
        line_dict = {}
        line_dict['name']= each.name
        line_dict['address'] = each.address
        line_dict['city'] = each.city
        line_dict['state'] = each.state
        line_dict['zipcode'] = str(each.zipcode).replace("<ImageFieldFile:","").replace(">","")
        line_dict['img_url'] = str(each.img_url).replace("<ImageFieldFile:","").replace(">","")
        line_dict['author'] = each.author
        line_dict['categories'] = each.categories
        line_list.append(line_dict)
    print(line_list)
    #line_list=serialize('json',  Post.objects.all().filter( name__icontains=q), cls=LazyEncoder)
    line_list=JsonResponse(line_list,safe=False)
    return render(request, 'result.html', {'post_list': post_list})

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