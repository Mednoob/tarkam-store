from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.core import serializers

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages

import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from main.models import Product
from main.forms import ProductForm

@login_required(login_url="/store/login")
def show_main(request: HttpRequest):
    context = {
        "app_name": "Tarkam Store",
        "name": "Ahmad Yaqdhan",
        "class": "PBP A",
        "npm": 2406399081,
        "message": "Coming soon!",
        "last_login": request.COOKIES.get("last_login", "Never"),
        "username": request.user.username
    }

    return render(request, "main.html", context)

@login_required(login_url="/store/login")
def show_product_list(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        "product_list": product_list
    }

    return render(request, "product_list.html", context)

@login_required(login_url="/store/login")
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()

        return redirect("main:show_main")

    context = {"form": form}
    return render(request, "create_product.html", context)

@login_required(login_url="/store/login")
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        "product": product
    }
    return render(request, "product_details.html", context)

def show_xml(request):
    products = Product.objects.all()
    data = serializers.serialize("xml", products)
    return HttpResponse(data, content_type="application/xml")

def show_json(request):
    products = Product.objects.all()
    data = serializers.serialize("json", products)
    return HttpResponse(data, content_type="application/json")

def show_xml_by_id(request, id):
    products = Product.objects.filter(pk=id)
    data = serializers.serialize("xml", products)
    return HttpResponse(data, content_type="application/xml")

def show_json_by_id(request, id):
    products = Product.objects.filter(pk=id)
    data = serializers.serialize("json", products)
    return HttpResponse(data, content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created")
            return redirect("main:login")

    context = { "form": form }
    return render(request, "register.html", context)

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie("last_login", str(datetime.datetime.now()))

            return response

    else:
        form = AuthenticationForm(request)

    context = { "form": form }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)

    response=HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")

    return response
