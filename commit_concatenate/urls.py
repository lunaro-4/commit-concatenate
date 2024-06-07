from django.urls import path
from .views import (show_table, show_home, register, login_form,
                    logout_form, get_github)


urlpatterns = [
    path("user/", show_table),
    path("", show_home, name="index"),
    path("reg/", register, name="reg"),
    path("login/", login_form, name="login"),
    path("logout", logout_form, name="logout"),
    path("api/github", get_github),
]
