from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from articles.models import Articulos, Categoria


class ArticuloTestData(TestCase):
    def setUp(self):
        self.autor = User.objects.create(
            username='autor', first_name='Ana', last_name='Pérez',
            email='ana@test.com'
        )
        self.otro = User.objects.create(
            username='otro', first_name='Luis', last_name='Gómez',
            email='luis@test.com'
        )
        self.categoria = Categoria.objects.create(name='Noticias')
        self.articulo = Articulos.objects.create(
            title='Título original',
            subtitle='Subtítulo',
            content='Contenido original',
            author=self.autor,
            category=self.categoria,
        )
        self.datos_form = {
            'title': 'Título nuevo',
            'subtitle': 'Subtítulo nuevo',
            'content': 'Contenido nuevo',
            'opcional_content': '',
            'category': self.categoria.pk,
        }


class ArticleDetailViewTests(ArticuloTestData):
    def test_detalle_status_y_template(self):
        response = self.client.get(reverse('articles:detalle', args=[self.articulo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_datail.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertEqual(response.context['articulo'], self.articulo)
        self.assertContains(response, 'Título original')

    def test_detalle_sin_botones_para_anonimo(self):
        response = self.client.get(reverse('articles:detalle', args=[self.articulo.pk]))
        self.assertNotContains(response, reverse('articles:editar', args=[self.articulo.pk]))
        self.assertNotContains(response, reverse('articles:eliminar', args=[self.articulo.pk]))

    def test_detalle_sin_botones_para_otro_usuario(self):
        self.client.force_login(self.otro)
        response = self.client.get(reverse('articles:detalle', args=[self.articulo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, reverse('articles:editar', args=[self.articulo.pk]))
        self.assertNotContains(response, reverse('articles:eliminar', args=[self.articulo.pk]))

    def test_detalle_con_botones_para_el_autor(self):
        self.client.force_login(self.autor)
        response = self.client.get(reverse('articles:detalle', args=[self.articulo.pk]))
        self.assertContains(response, reverse('articles:editar', args=[self.articulo.pk]))
        self.assertContains(response, reverse('articles:eliminar', args=[self.articulo.pk]))


class ArticleCreateViewTests(ArticuloTestData):
    def test_crear_requiere_login(self):
        response = self.client.get(reverse('articles:crear'))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('articles:crear')}"
        )

    def test_crear_get_como_autenticado(self):
        self.client.force_login(self.autor)
        response = self.client.get(reverse('articles:crear'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_create.html')
        self.assertContains(response, 'Crear Nuevo Artículo')

    def test_crear_post_guarda_y_asigna_autor(self):
        self.client.force_login(self.otro)
        cantidad_antes = Articulos.objects.count()
        response = self.client.post(reverse('articles:crear'), self.datos_form)
        self.assertRedirects(response, reverse('core:home'))
        self.assertEqual(Articulos.objects.count(), cantidad_antes + 1)
        nuevo = Articulos.objects.get(title='Título nuevo')
        self.assertEqual(nuevo.author, self.otro)
        self.assertEqual(nuevo.category, self.categoria)

    def test_crear_post_invalido_no_guarda(self):
        self.client.force_login(self.autor)
        cantidad_antes = Articulos.objects.count()
        response = self.client.post(reverse('articles:crear'), {'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Articulos.objects.count(), cantidad_antes)


class ArticleUpdateViewTests(ArticuloTestData):
    def test_editar_requiere_login(self):
        url = reverse('articles:editar', args=[self.articulo.pk])
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={url}")

    def test_editar_prohibido_para_otro_usuario(self):
        self.client.force_login(self.otro)
        response = self.client.get(reverse('articles:editar', args=[self.articulo.pk]))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('articles:editar', args=[self.articulo.pk]), self.datos_form)
        self.assertEqual(response.status_code, 403)
        self.articulo.refresh_from_db()
        self.assertEqual(self.articulo.title, 'Título original')

    def test_editar_get_autor_form_precargado(self):
        self.client.force_login(self.autor)
        response = self.client.get(reverse('articles:editar', args=[self.articulo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_update.html')
        self.assertContains(response, 'Título original')
        self.assertContains(response, 'Guardar Cambios')

    def test_editar_post_autor_modifica_articulo(self):
        self.client.force_login(self.autor)
        response = self.client.post(reverse('articles:editar', args=[self.articulo.pk]), self.datos_form)
        self.assertRedirects(response, reverse('articles:mis-articulos'))
        self.articulo.refresh_from_db()
        self.assertEqual(self.articulo.title, 'Título nuevo')
        self.assertEqual(self.articulo.content, 'Contenido nuevo')
        self.assertEqual(self.articulo.author, self.autor)


class ArticleDeleteViewTests(ArticuloTestData):
    def test_eliminar_requiere_login(self):
        url = reverse('articles:eliminar', args=[self.articulo.pk])
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={url}")

    def test_eliminar_prohibido_para_otro_usuario(self):
        self.client.force_login(self.otro)
        response = self.client.get(reverse('articles:eliminar', args=[self.articulo.pk]))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('articles:eliminar', args=[self.articulo.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Articulos.objects.filter(pk=self.articulo.pk).exists())

    def test_eliminar_get_autor_pide_confirmacion(self):
        self.client.force_login(self.autor)
        response = self.client.get(reverse('articles:eliminar', args=[self.articulo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_delete.html')
        self.assertContains(response, 'Eliminar Artículo')
        self.assertContains(response, 'Sí, eliminar artículo')

    def test_eliminar_post_autor_borra_articulo(self):
        self.client.force_login(self.autor)
        pk = self.articulo.pk
        response = self.client.post(reverse('articles:eliminar', args=[pk]))
        self.assertRedirects(response, reverse('articles:mis-articulos'))
        self.assertFalse(Articulos.objects.filter(pk=pk).exists())


class MisArticulosTests(ArticuloTestData):
    def test_mis_articulos_requiere_login(self):
        url = reverse('articles:mis-articulos')
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={url}")

    def test_mis_articulos_status_y_template(self):
        self.client.force_login(self.autor)
        response = self.client.get(reverse('articles:mis-articulos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/mis_articulos.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_mis_articulos_solo_muestra_los_propios(self):
        Articulos.objects.create(
            title='Artículo de Luis',
            content='Contenido de Luis',
            author=self.otro,
            category=self.categoria,
        )
        self.client.force_login(self.autor)
        response = self.client.get(reverse('articles:mis-articulos'))
        self.assertContains(response, 'Título original')
        self.assertNotContains(response, 'Artículo de Luis')
        self.assertEqual(len(response.context['articulos']), 1)
        self.assertIn(self.articulo, list(response.context['articulos']))

    def test_mis_articulos_vacio_muestra_estado_inicial(self):
        self.client.force_login(self.otro)
        response = self.client.get(reverse('articles:mis-articulos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Todavía no publicaste artículos.')
        self.assertNotContains(response, 'Título original')

    def test_mis_articulos_incluye_acciones_editar_eliminar(self):
        self.client.force_login(self.autor)
        response = self.client.get(reverse('articles:mis-articulos'))
        self.assertContains(response, reverse('articles:editar', args=[self.articulo.pk]))
        self.assertContains(response, reverse('articles:eliminar', args=[self.articulo.pk]))
        self.assertContains(response, reverse('articles:detalle', args=[self.articulo.pk]))

    def test_nuevo_articulo_aparece_en_el_panel(self):
        self.client.force_login(self.otro)
        self.client.post(reverse('articles:crear'), self.datos_form)
        response = self.client.get(reverse('articles:mis-articulos'))
        self.assertContains(response, 'Título nuevo')
