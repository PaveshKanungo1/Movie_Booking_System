from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from admin_app.models import Movie
from rest_framework.authtoken.models import Token

class MovieAdminTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', is_staff=True)
        self.token = Token.objects.create(user=self.admin_user)
        
        self.non_admin_user = User.objects.create_user(username='user', password='userpassword')
        self.non_admin_token = Token.objects.create(user=self.non_admin_user)

    def test_admin_can_create_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            'title': 'Inception',
            'description': 'A mind-bending thriller.',
            'release_date': '2010-07-16'
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 1)

    def test_non_admin_cannot_create_movie(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.non_admin_token.key)
        data = {
            'title': 'Inception',
            'description': 'A mind-bending thriller.',
            'release_date': '2010-07-16'
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_movie(self):
        movie = Movie.objects.create(title='Inception', description='A mind-bending thriller.', release_date='2010-07-16')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'title': 'Inception Updated'}
        response = self.client.patch(f'/api/movies/{movie.pk}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movie.refresh_from_db()
        self.assertEqual(movie.title, 'Inception Updated')

    def test_admin_can_delete_movie(self):
        movie = Movie.objects.create(title='Inception', description='A mind-bending thriller.', release_date='2010-07-16')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(f'/api/movies/{movie.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)

    def test_non_admin_cannot_delete_movie(self):
        movie = Movie.objects.create(title='Inception', description='A mind-bending thriller.', release_date='2010-07-16')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.non_admin_token.key)
        response = self.client.delete(f'/api/movies/{movie.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
