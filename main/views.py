from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.core import serializers
from main.models import Product
from main.forms import ProductForm

def show_main(request: HttpRequest):
    context = {
        "app_name": "Tarkam Store",
        "name": "Ahmad Yaqdhan",
        "class": "PBP A",
        "npm": 2406399081,
        "message": "Coming soon!"
    }

    return render(request, "main.html", context)

def show_product_list(request):
    product_list = Product.objects.all()

    context = {
        "product_list": product_list
    }

    return render(request, "product_list.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:show_main")

    context = {"form": form}
    return render(request, "create_product.html", context)

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
