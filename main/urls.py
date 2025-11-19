from django.urls import path

from main.views import show_main, show_product_list, show_product
from main.views import show_xml, show_json, show_xml_by_id, show_json_by_id
from main.views import add_product_ajax, edit_product_ajax, delete_product_ajax, register_ajax, login_ajax, logout_ajax
from main.views import proxy_image, create_product_flutter, get_products_flutter

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("products/", show_product_list, name="show_product_list"),
    path("products/<str:id>/", show_product, name="show_product"),

    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<str:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<str:id>/", show_json_by_id, name="show_json_by_id"),

    path("register/", register_ajax, name="register"),
    path("login/", login_ajax, name="login"),
    path("logout/", logout_ajax, name="logout"),

    path("create-product-ajax/", add_product_ajax, name="add_product_ajax"),
    path("edit-product-ajax/<uuid:id>", edit_product_ajax, name="edit_product_ajax"),
    path("delete-product-ajax/<uuid:id>", delete_product_ajax, name="delete_product_ajax"),

    path("proxy-image/", proxy_image, name="proxy_image"),
    path("create-flutter/", create_product_flutter, name="create_product_flutter"),
    path("get-flutter/", get_products_flutter, name="get_products_flutter")
]
