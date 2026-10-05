from django.urls import path

from articles.views import ArticleDetailView,ArticleCreateView

app_name= 'articles'

urlpatterns = [
    path('detalle/<int:pk>/', ArticleDetailView.as_view(),name="detalle" ),
    path('crear/', ArticleCreateView.as_view(), name='crear'),
]