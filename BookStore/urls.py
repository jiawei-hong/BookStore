"""BookStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from tenlong import views as tl_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tl_views.index),
    path('keywordResult', tl_views.get_keyword),
    path('special/<int:special_id>', tl_views.special),
    path('special/<int:special_id>/<int:page>', tl_views.get_special_books),
    path('publishers', tl_views.get_publisher),
    path('publishers/<int:publisher_id>', tl_views.publisher),
    path('publishers/<int:publisher_id>/<int:page>', tl_views.get_publisher_books),
]
