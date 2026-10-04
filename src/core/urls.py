from django.urls import path
from core.views import Inicio

app_name= 'core'

urlpatterns = [
    path('',Inicio,name="home"),
]