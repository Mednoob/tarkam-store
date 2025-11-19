import django.urls as urls
from authentication.views import login, register, logout

app_name = "authentication"

urlpatterns = [
    urls.path("login/", login, name="login"),
    urls.path("register/", register, name="register"),
    urls.path("logout/", logout, name="logout"),
]
