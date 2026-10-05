from django.shortcuts import render
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from articles.models import Articulos
from articles.forms import ArticuloForm


class ArticleDetailView(DetailView):
    model = Articulos
    template_name = 'articles/article_datail.html'
    context_object_name = 'articulo'

class ArticleCreateView( LoginRequiredMixin,CreateView):
    model = Articulos
    form_class = ArticuloForm
    template_name = 'articles/article_create.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
            form.instance.author = self.request.user  # Asigna el usuario logueado como autor
            return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articulos
    form_class = ArticuloForm
    template_name = 'articles/article_update.html'
    success_url = reverse_lazy('articles:mis-articulos')

    def test_func(self):
        articulo = self.get_object()
        return self.request.user == articulo.author or self.request.user.is_staff


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articulos
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('articles:mis-articulos')

    def test_func(self):
        articulo = self.get_object()
        return self.request.user == articulo.author or self.request.user.is_staff


class MisArticulosView(LoginRequiredMixin, ListView):
    model = Articulos
    template_name = 'articles/mis_articulos.html'
    context_object_name = 'articulos'

    def get_queryset(self):
        return Articulos.objects.filter(author=self.request.user).order_by('-crated_at')