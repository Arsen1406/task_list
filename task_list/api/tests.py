import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_list.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework import status
from tasks.models import Task
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient

User = get_user_model()


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.data = {
            'username': 'TestUser',
            'password': 'testpass',
            'email': 'test@mail.ru'
        }
        self.user = User.objects.create(**self.data)
        self.token = self.client.post(
            '/api/v1/auth/token/',
            self.data,
            format='json'
        ).data.get('token')

    def test_create_user(self):
        url = '/api/v1/auth/signup/'
        data = {
            'username': 'TestUser2',
            'password': 'testpass2',
            'email': 'test2@mail.ru'
        }

        response = self.client.post(url, data, format='json')
        user = User.objects.filter(username='TestUser2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(user), 1)
        self.assertEqual(user.first().email, 'test2@mail.ru')
        self.assertEqual(user.first().username, 'TestUser2')

    def test_get_token(self):
        url = '/api/v1/auth/token/'
        data = {
            'username': 'TestUser',
            'password': 'testpass',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('token'), None)

    def test_get_user_me(self):
        url = '/api/v1/users/me/'
        client = APIClient()
        client.force_authenticate(user=self.user, token=self.token)
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username'), 'TestUser')
        self.assertEqual(response.data.get('email'), 'test@mail.ru')


class TaskTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.data = {
            'username': 'TestUser',
            'password': 'testpass',
            'email': 'test@mail.ru'
        }
        self.user = User.objects.create(**self.data)
        self.token = self.client.post(
            '/api/v1/auth/token/',
            self.data,
            format='json'
        ).data.get('token')
        self.task = Task.objects.create(user=self.user)
        self.client_auth = APIClient()
        self.task = Task.objects.filter(user=self.user).first()

    def test_get_all_task(self):
        url = '/api/v1/tasks/'
        self.client_auth.force_authenticate(
            user=self.user,
            token=self.token
        )
        response = self.client_auth.get(url, format='json')
        data = response.data.get('results')[0]

        self.assertTrue(isinstance(response.data.get('results'), list))
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('status'), 'create')
        self.assertEqual(data.get('user').get('username'), self.user.username)

    def test_get_task_in_processing(self):
        url = f'/api/v1/processing/{self.task.pk}/'
        self.client_auth.force_authenticate(
            user=self.user,
            token=self.token
        )
        response = self.client_auth.get(url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('status'), 'create')
        self.assertEqual(data.get('user').get('username'), self.user.username)

    def test_get_change_status_in_processing(self):
        pk = self.task.pk
        url = f'/api/v1/processing/{pk}/'
        self.client_auth.force_authenticate(
            user=self.user,
            token=self.token
        )

        response = self.client_auth.patch(url, format='json')
        task = Task.objects.get(pk=pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Процесс обработки запущен!')
        self.assertEqual(task.status, 'processing')
        self.assertEqual(task.user.username, self.user.username)

    def test_get_task_in_answer(self):
        self.task.status = 'processing'
        self.task.save()

        url = f'/api/v1/answer/{self.task.pk}/'
        self.client_auth.force_authenticate(
            user=self.user,
            token=self.token
        )
        response = self.client_auth.get(url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('status'), 'processing')
        self.assertEqual(data.get('user').get('username'), self.user.username)

    def test_get_change_status_in_answer(self):
        self.task.status = 'processing'
        self.task.save()

        url = f'/api/v1/answer/{self.task.pk}/'
        self.client_auth.force_authenticate(
            user=self.user,
            token=self.token
        )

        response = self.client_auth.patch(url, format='json')
        task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Процесс обработки запущен!')
        self.assertEqual(task.status, 'answer')
        self.assertEqual(task.user.username, self.user.username)



