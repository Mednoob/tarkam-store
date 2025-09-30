from django.urls import path
from main.views import show_main, show_product_list, create_product, show_product, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_product, delete_product

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("create-product/", create_product, name="create_product"),
    path("products/", show_product_list, name="show_product_list"),
    path("products/<str:id>/", show_product, name="show_product"),

    path("xml/", show_xml, name="show_xml"),
    path("json/", show_json, name="show_json"),
    path("xml/<str:id>/", show_xml_by_id, name="show_xml_by_id"),
    path("json/<str:id>/", show_json_by_id, name="show_json_by_id"),

    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("products/<uuid:id>/edit/", edit_product, name="edit_product"),
    path("products/<uuid:id>/delete/", delete_product, name="delete_product")
]
