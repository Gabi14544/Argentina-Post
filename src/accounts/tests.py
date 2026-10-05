from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

# PBKDF2 tarda ~5s por usuario en esta máquina: en tests usamos MD5 (solo tests).
HASHERS_RAPIDOS = ['django.contrib.auth.hashers.MD5PasswordHasher']

class AccountsViewsTests(TestCase):
    def test_login_view_status_and_template(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'accounts/css/style.css')
        self.assertContains(response, 'auth-card')
        self.assertContains(response, 'btn-comic')
        self.assertContains(response, 'Iniciar Sesión')

    def test_registro_view_status_and_template(self):
        response = self.client.get(reverse('accounts:registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/registro.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'accounts/css/style.css')
        self.assertContains(response, 'auth-card')
        self.assertContains(response, 'btn-comic')
        self.assertContains(response, 'Registrate como POST')


@override_settings(PASSWORD_HASHERS=HASHERS_RAPIDOS)
class RegistroTests(TestCase):
    datos = {
        'username': 'nuevo_user',
        'first_name': 'Nuevo',
        'last_name': 'Usuario',
        'email': 'nuevo@test.com',
        'password1': 'P4ssw0rd-segura',
        'password2': 'P4ssw0rd-segura',
    }

    def test_registro_post_valido_crea_usuario_y_redirige_a_login(self):
        response = self.client.post(reverse('accounts:registro'), self.datos)
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertTrue(User.objects.filter(username='nuevo_user').exists())
        usuario = User.objects.get(username='nuevo_user')
        self.assertEqual(usuario.first_name, 'Nuevo')
        self.assertEqual(usuario.last_name, 'Usuario')
        self.assertEqual(usuario.email, 'nuevo@test.com')
        self.assertTrue(usuario.check_password('P4ssw0rd-segura'))

    def test_registro_post_passwords_distintos_no_crea_usuario(self):
        datos = {**self.datos, 'password2': 'otra-password'}
        response = self.client.post(reverse('accounts:registro'), datos)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='nuevo_user').exists())


@override_settings(PASSWORD_HASHERS=HASHERS_RAPIDOS)
class LoginLogoutTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='cliente', first_name='Cla', last_name='Ríos',
            email='cla@test.com', password='secreta123'
        )

    def test_login_post_autentica_y_redirige_a_home(self):
        response = self.client.post(
            reverse('accounts:login'),
            {'username': 'cliente', 'password': 'secreta123'},
        )
        self.assertRedirects(response, reverse('core:home'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_post_cierra_sesion(self):
        self.client.login(username='cliente', password='secreta123')
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('core:home'))
        self.assertNotIn('_auth_user_id', self.client.session)
