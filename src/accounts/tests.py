from django.test import TestCase
from django.urls import reverse

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
