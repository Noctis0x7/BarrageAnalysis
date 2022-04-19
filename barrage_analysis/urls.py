"""barrage_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from barrage import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index),
    path('crawl', views.barrage_crawl),
    path('upload', views.upload),
    path('upload_file', views.upload_file),
    path('preprocess_storage', views.preprocess_store),
    path('preprocess', views.preprocess),
    path('store', views.store),
    path('analysis', views.analysis),
    path('result', views.result)
]
