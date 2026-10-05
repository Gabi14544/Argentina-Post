from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from articles.models import Articulos, Categoria


class CorePortadaTests(TestCase):
    def setUp(self):
        self.autor = User.objects.create(
            username='autor_portada', first_name='Ana', last_name='Pérez', email='ana@test.com'
        )
        self.categoria = Categoria.objects.create(name='Noticias')
        self.articulo = Articulos.objects.create(
            title='Primer artículo',
            subtitle='Subtítulo del primero',
            content='Contenido principal',
            author=self.autor,
            category=self.categoria,
        )

    def test_portada_status_y_templates(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_portada_muestra_articulos(self):
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'Primer artículo')
        self.assertContains(response, 'Noticias')
        self.assertContains(response, reverse('articles:detalle', args=[self.articulo.pk]))

    def test_portada_estado_vacio(self):
        Articulos.objects.all().delete()
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'No hay artículos disponibles')

    def test_nav_anonimo_no_muestra_crud(self):
        response = self.client.get(reverse('core:home'))
        self.assertNotContains(response, reverse('articles:crear'))
        self.assertContains(response, reverse('accounts:login'))
        self.assertContains(response, reverse('accounts:registro'))

    def test_nav_autenticado_muestra_crud(self):
        self.client.force_login(self.autor)
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, reverse('articles:crear'))
        self.assertNotContains(response, reverse('accounts:login'))
