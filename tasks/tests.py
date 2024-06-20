from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TasksTestCase(TestCase):
    fixtures = ['fixtures/test/movieModel.json', 'fixtures/languageModel.json']

    def setUp(self):
        self.client = APIClient()

    def test_get_movies(self):
        response = self.client.get('/v1/api/movies/get_movies/')
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_200_OK)
        self.assertEqual(data['error'], False)
        self.assertIn('responseData', data)
        self.assertIn('results', data['responseData'])

        fields = ['id', 'name', 'director', 'release_year', 'language', 'language_name', 'rating']
        for field in fields:
            self.assertIn(field, data['responseData']['results'][0])

    def test_add_movie_pass(self):
        response = self.client.get('/v1/api/movies/add_movie/')
        data = {
            "name": "Wanted2",
            "director": "Prabhu Deva",
            "release_year": 2014,
            "language": "hi",
            "rating": 9.5
        }

        response = self.client.post('/v1/api/movies/add_movie/', data)
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_200_OK)
        self.assertEqual(data['error'], False)
        self.assertEqual(data['responseData'], 'Data Added Successfully')

    def test_add_movie_failed(self):
        response = self.client.get('/v1/api/movies/add_movie/')
        data = {
            "name": "Wanted2",
            "director": "Prabhu Deva",
            "release_year": 2014,
            "language": "english",
            "rating": 9.5
        }

        response = self.client.post('/v1/api/movies/add_movie/', data)
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data['error'], True)

    def test_update_movie_pass(self):
        response = self.client.get('/v1/api/movies/update_movie/')
        data = {
            "id": 2,
            "rating": 9
        }

        response = self.client.patch('/v1/api/movies/update_movie/', data)
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_200_OK)
        self.assertEqual(data['error'], False)
        self.assertEqual(data['responseData'], 'Data Updated Successfully')

    def test_update_movie_fail(self):
        response = self.client.get('/v1/api/movies/update_movie/')
        data = {
            "id": 1,
            "rating": 9
        }

        response = self.client.patch('/v1/api/movies/update_movie/', data)
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data['error'], True)

    def test_delete_movie_pass(self):
        _id = 2
        response = self.client.delete(f'/v1/api/movies/delete_movie/?id={_id}')
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_200_OK)
        self.assertEqual(data['error'], False)
        self.assertEqual(data['responseData'], 'Data Deleted Successfully')

    def test_delete_movie_fail(self):
        _id = 1
        response = self.client.delete(f'/v1/api/movies/delete_movie/?id={_id}')
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data['error'], True)

    def test_get_language_codes(self):
        response = self.client.get('/v1/api/movies/get_language_codes/')
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_200_OK)
        self.assertEqual(data['error'], False)
        self.assertIn('responseData', data)
        self.assertIn('code', data['responseData'][0])
        self.assertIn('name', data['responseData'][0])

    def test_get_movies_count_by_language(self):
        language_code = 'en'
        response = self.client.get(f'/v1/api/movies/get_movies_count_by_language/?language_code={language_code}')
        data = response.data
        self.assertEqual(data['status_code'], status.HTTP_200_OK)
        self.assertEqual(data['error'], False)
        self.assertIn('responseData', data)
        self.assertIn('count', data['responseData'])
