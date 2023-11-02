from django.urls import path
from .views import *


urlpatterns = [
        path('user/', show_table),
        path('', show_home, name='index'),
        path('reg/', register, name='reg'),
        path('login/', login_form, name='login'),
        path('logout', logout_form, name='logout'),

]
