from django.urls import path

from articles.views import ArticleDetailView

app_name= 'articles'

urlpatterns = [
    path('detalle/<int:pk>/', ArticleDetailView.as_view(),name="detalle" ),
]