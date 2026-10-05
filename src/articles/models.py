from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Articulos(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length = 200, blank=True)
    content = models.TextField()
    opcional_content = models.TextField(blank=True,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Categoria,on_delete = models.CASCADE)
    crated_at =models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Articulo"
        verbose_name_plural = "Articulos"

        

    def __str__(self):
        return self.title
    