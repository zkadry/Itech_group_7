from django.test import TestCase

# Create your tests here.
# Inside tests.py or within the tests module, e.g., tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


User = get_user_model()

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        # Data for user registration
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complex_password',
            'password2': 'complex_password',
        }
        response = self.client.post(reverse('signup'), data)
        # Check for redirect status code (302 means success and redirected)
        self.assertEqual(response.status_code, 302)
        # Check if the user was successfully created
        self.assertTrue(User.objects.filter(username='testuser').exists())

class UserLoginTest(TestCase):
    def setUp(self):
        # Create a user before the test
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='complex_password')

    def test_login_with_valid_credentials(self):
        # Log in with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'complex_password'})
        # Check for redirect status code
        self.assertEqual(response.status_code, 302)
        # Check if the user is authenticated
        user = authenticate(username='testuser', password='complex_password')
        self.assertTrue(user is not None and user.is_authenticated)

    def test_login_with_invalid_credentials(self):
        # Attempt to log in with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        # Check for failure status code or error message
        # self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        self.assertEqual(response.context['error'], 'Invalid username or password.')