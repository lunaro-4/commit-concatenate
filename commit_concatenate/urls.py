from django.urls import path
from .views import *


urlpatterns = [
        path('user/', show_tabel),
        path('', show_home),
]
