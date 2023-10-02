from django.urls import path
from .views import form_table 


urlpatterns = [
        path('', form_table)
]
