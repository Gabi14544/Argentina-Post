from django.shortcuts import render
from django.views.generic import DetailView
from articles.models import Articulos



class ArticleDetailView(DetailView):
    model = Articulos
    template_name = 'article/article_detail.html'
    context_object_name = 'articulo'

    