from django.shortcuts import render
from django.views.generic import DetailView
from articles.models import Articulos



class ArticleDetailView(DetailView):
    model = Articulos
    template_name = 'articles/article_datail.html'
    context_object_name = 'articulo'

    