"""websystemdesign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cmdb import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
urlpatterns = [
    #path('admin/', admin.site.urls),
    path(r'index.html',views.index),
    path(r'login.html', views.login_view,name="login"),
    path(r'account.html', views.account),
    path(r'account/uploadImg.html', views.uploadImg),
    path('showImg/', views.showImg),
    #path('order/', views.order),
    path('search/', views.search),
    path('result/', views.result),
    path('allpicture/', views.showImg),
    path('logout.html', views.logout_view),
    path('register.html', views.register_view,name='register'),
    path('register/regist_succusess.html', views.regist_succusess),
    path('category.html', views.category),
    path('animals.html', views.animals),
    path('landscapes.html', views.landscapes),
    path('other.html', views.other),
    path('food.html', views.food),
    path('portrait.html', views.portrait),
    path('architecture.html', views.architecture),
    path('viewimge/', views.viewimge,name='data'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
