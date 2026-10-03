from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from articles.models import Articulos



def listar_articulos(request:HttpRequest) ->HttpResponse:
    articulos = Articulos.objects.all()
    return render(request,'core/index.html', {"articulo":articulos})
