"""sparrow_crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    url(r'^$', views.index, {'template_name': 'index.html'}),
    url(r'^api/sparrow_crawl/t/document/$', views.index, {'template_name': 'document.html'}),
    url(r'^api/sparrow_crawl/t/brand/list/', views.index, {'template_name': 'brand/brandlist.html'}),
    url(r'^api/sparrow_crawl/t/product/list/', views.index, {'template_name': 'product/productlist.html'}),
    url(r'^api/sparrow_crawl/t/task/list/', views.index, {'template_name': 'task/tasklist.html'}),
    path('admin/', admin.site.urls),
    url(r'^api/sparrow_crawl/site/', include('adminsite.urls', namespace="crawl_site_api")),
]
