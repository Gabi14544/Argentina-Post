from django.urls import path

from articles.views import ArticleDetailView,ArticleCreateView,ArticleUpdateView,ArticleDeleteView,MisArticulosView

app_name= 'articles'

urlpatterns = [
    path('detalle/<int:pk>/', ArticleDetailView.as_view(),name="detalle" ),
    path('crear/', ArticleCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', ArticleUpdateView.as_view(), name='editar'),
    path('eliminar/<int:pk>/', ArticleDeleteView.as_view(), name='eliminar'),
    path('mis-articulos/', MisArticulosView.as_view(), name='mis-articulos'),
]
