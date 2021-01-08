from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.forms.models import model_to_dict
from .models import Books
import json


# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)

        return HttpResponseRedirect('/')

    return render(request, 'users/login.html')


def logout(request):
    auth.logout(request)

    return HttpResponseRedirect('/')


def get_user_products(request, user_id):
    user_products = [model_to_dict(data) for data in Books.objects.filter(user_id=user_id)]

    return HttpResponse(json.dumps(user_products))


def add_products(request, product_id):
    Books.objects.create(user_id=request.user, product_id=product_id)

    return HttpResponse(json.dumps({
        'msg': 'Create Success'
    }))


def delete_product(request, product_id):
    Books.objects.get(user_id=request.user, product_id=product_id).delete()

    return HttpResponse(json.dumps({
        'msg': 'Delete Success'
    }))
