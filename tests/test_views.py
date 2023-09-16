from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegistrationViewTest(TestCase):

    def post(self):
        url = reverse('register')
        data = {
            'email': 'lc@gmail.com',
            settings.HONEYPOT_FIELD_NAME: ''
        }

        response = self.client.post(url, data=data)
        return response

    def test_honeypot_required(self):
        url = reverse('register')

        # Post without the secret honeypot should return a HTTP 400 Bad Request
        res = self.client.post(url, data={'email': 'lc@gmail.com'})

        self.assertEqual(res.status_code, 400)
        self.assertIn('Honey Pot Error', res.content)

    def test_post(self):
        expected_redirect_url = reverse('registration_complete')
        res = self.post()

        # Verify user is redirected properly after providing email
        self.assertRedirects(res, expected_redirect_url)

    def test_inactive_user_created(self):
        self.assertEqual(User.objects.count(), 0)

        self.post()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, 'lc@gmail.com')
        self.assertFalse(User.objects.first().is_active)

    def test_account_activation_email_sent(self):
        self.post()

        # Test that one email has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Account activation')

        # Verify email sent to address provided
        self.assertEqual(mail.outbox[0].to, ['lc@gmail.com', ])
