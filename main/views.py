from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core import serializers

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from main.models import Product

import json
from django.utils.html import strip_tags

import requests

@login_required(login_url="/store/login")
def show_main(request: HttpRequest):
    context = {
        "user": request.user,
        "last_login": request.COOKIES.get("last_login", "Never")
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
        "product_list": product_list,
        "last_login": request.COOKIES.get("last_login", "Never")
    }

    return render(request, "product_list.html", context)

@login_required(login_url="/store/login")
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        "product": product
    }
    return render(request, "product_details.html", context)

@login_required(login_url="/store/login")
@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponse(b"OK", status=200)

@login_required(login_url="/store/login")
@csrf_exempt
@require_POST
def add_product_ajax(request: HttpRequest):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == "on"
    user = request.user

    new_product = Product(
        name=name,
        price=price,
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url="/store/login")
@csrf_exempt
@require_POST
def edit_product_ajax(request: HttpRequest, id):
    try:
        product = Product.objects.select_related("user").filter(pk=id).get()

        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        category = request.POST.get("category")
        thumbnail = request.POST.get("thumbnail")
        is_featured = request.POST.get("is_featured") == "on"

        product.name = name
        product.price = price
        product.description = description
        product.category = category
        product.thumbnail = thumbnail
        product.is_featured = is_featured

        product.save()
        return HttpResponse(b"OK", status=200)
    except Exception as e:
        return HttpResponse(f"{str(e)}", status=500)

def show_xml(request):
    products = Product.objects.all()
    data = serializers.serialize("xml", products)
    return HttpResponse(data, content_type="application/xml")

def show_json(request):
    products = Product.objects.all()
    data = [
        {
            "id": str(product.id),
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "thumbnail": product.thumbnail,
            "category": product.category,
            "is_featured": product.is_featured,
            "user_id": product.user_id
        }
        for product in products
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    products = Product.objects.filter(pk=id)
    data = serializers.serialize("xml", products)
    return HttpResponse(data, content_type="application/xml")

def show_json_by_id(request, id):
    try:
        product = Product.objects.select_related("user").filter(pk=id).get()
        data = {
            "id": str(product.id),
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "thumbnail": product.thumbnail,
            "category": product.category,
            "is_featured": product.is_featured,
            "user_id": product.user_id,
            "user_username": product.user.username if product.user_id else None
        }

        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({ "detail": "Not Found" }, status=404)

@csrf_exempt
def register_ajax(request: HttpRequest):
    if request.method != "POST":
        return render(request, "register.html", {})

    username = request.POST.get("username")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    form = UserCreationForm({
        "username": username,
        "password1": password1,
        "password2": password2
    })

    if form.is_valid():
        form.save()
        return HttpResponse(b"CREATED", status=201)
    else:
        non_field_errors = []
        field_errors = []

        for error in form.non_field_errors():
            non_field_errors.append(str(error))

        for field, errors in form.errors.items():
            if field == "__all__": continue

            for error in errors:
                field_errors.append({ "field": field, "error": str(error) })

        return JsonResponse({
            "non_field_errors": non_field_errors,
            "field_errors": field_errors
        }, status=400)

@csrf_exempt
def login_ajax(request: HttpRequest):
    if request.method != "POST":
        return render(request, "login.html", {})

    username = request.POST.get("username")
    password = request.POST.get("password")

    form = AuthenticationForm(data={
        "username": username,
        "password": password
    })

    if form.is_valid():
        user = form.get_user()
        login(request, user)

        response = HttpResponse(b"OK", status=200)
        response.set_cookie("last_login", str(datetime.datetime.now()))

        return response
    else:
        non_field_errors = []
        field_errors = []

        for error in form.non_field_errors():
            non_field_errors.append(str(error))

        for field, errors in form.errors.items():
            if field == "__all__": continue

            for error in errors:
                field_errors.append({ "field": field, "error": str(error) })

        return JsonResponse({
            "non_field_errors": non_field_errors,
            "field_errors": field_errors
        }, status=400)

@csrf_exempt
def logout_ajax(request):
    logout(request)

    response=HttpResponse(b"OK", status=200) if request.method == "POST" else HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")

    return response

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get('name', ''))
        price = data.get('price', 0)
        description = strip_tags(data.get('description', ''))
        category = strip_tags(data.get('category', ''))
        thumbnail = strip_tags(data.get('thumbnail', ''))
        is_featured = data.get('is_featured', False)
        user = request.user

        new_product = Product(
            name=name,
            price=price,
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)

@csrf_exempt
def get_products_flutter(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = [
            {
                "id": str(product.id),
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "thumbnail": product.thumbnail,
                "category": product.category,
                "is_featured": product.is_featured,
                "user_id": product.user_id
            }
            for product in products
        ]

        filter = request.GET.get('filter', 'all')
        if filter != 'all':
            user_id = request.user.id
            data = [product for product in data if product['user_id'] == user_id]

        return JsonResponse(data, safe=False, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
