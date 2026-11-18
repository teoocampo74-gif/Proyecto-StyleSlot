from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse


class LoginViewTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            username='estilista',
            password='ClaveSegura123!',
        )

    def test_login_page_uses_gestion_template(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gestion/login.html')

    def test_homepage_is_barberpro_and_dashboard_remains_available(self):
        homepage = self.client.get(reverse('inicio'))
        dashboard = self.client.get(reverse('panel'))

        self.assertEqual(homepage.status_code, 200)
        self.assertTemplateUsed(homepage, 'gestion/barberpro.html')
        self.assertContains(homepage, f'href="{reverse("login")}"')
        self.assertContains(homepage, f'href="{reverse("registro")}"')
        self.assertEqual(dashboard.status_code, 200)
        self.assertTemplateUsed(dashboard, 'gestion/inicio.html')

    def test_registration_page_renders(self):
        response = self.client.get(reverse('registro'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gestion/registro.html')

    def test_valid_credentials_log_in_and_redirect_to_home(self):
        response = self.client.post(reverse('login'), {
            'username': 'estilista',
            'password': 'ClaveSegura123!',
        })

        self.assertRedirects(response, reverse('inicio'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_credentials_show_an_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'estilista',
            'password': 'incorrecta',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].non_field_errors())

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        EMAIL_HOST_USER='styleslot@example.com',
        EMAIL_HOST_PASSWORD='app-password',
        DEFAULT_FROM_EMAIL='styleslot@example.com',
        REGISTRATION_NOTIFICATION_EMAIL='admin@example.com',
    )
    def test_registration_creates_user_and_emails_details_without_password(self):
        response = self.client.post(reverse('registro'), {
            'nombre': 'Ana Pérez',
            'username': 'ana',
            'email': 'ana@example.com',
            'telefono': '3001234567',
            'password1': 'ClaveSegura123!abc',
            'password2': 'ClaveSegura123!abc',
        })

        self.assertRedirects(response, reverse('login'))
        user = get_user_model().objects.get(username='ana')
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('ClaveSegura123!abc'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['admin@example.com'])
        self.assertIn('Ana Pérez', mail.outbox[0].body)
        self.assertIn('3001234567', mail.outbox[0].body)
        self.assertNotIn('ClaveSegura123!abc', mail.outbox[0].body)

    @override_settings(
        EMAIL_HOST_USER='',
        EMAIL_HOST_PASSWORD='',
        REGISTRATION_NOTIFICATION_EMAIL='',
    )
    def test_registration_is_not_saved_if_email_is_not_configured(self):
        response = self.client.post(reverse('registro'), {
            'nombre': 'Ana Pérez',
            'username': 'ana',
            'email': 'ana@example.com',
            'telefono': '3001234567',
            'password1': 'ClaveSegura123!abc',
            'password2': 'ClaveSegura123!abc',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertFalse(get_user_model().objects.filter(username='ana').exists())
