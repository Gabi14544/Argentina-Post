from django.urls import path
from core.views import listar_articulos

app_name= 'core'

urlpatterns = [
    path('', listar_articulos,name="home"),
]