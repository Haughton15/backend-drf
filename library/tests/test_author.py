from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models.author import Author
import os

class AuthorViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('author-list') 
        self.sample_image = SimpleUploadedFile(
            name='Frieren.jpg',
            content=open('library/tests/test_files/Frieren.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        
        # Datos de prueba
        self.valid_data = {
            'name': 'Howard Phillips Lovecraft',
            'birth_date': '1937-03-15',
            'photo': self.sample_image
        }
        
        self.invalid_data = {
            'name': '',
            'birth_date': '1937-03-15'
        }

    def tearDown(self):
        # Limpiar archivos subidos después de cada test
        for author in Author.objects.all():
            if author.photo:
                if os.path.isfile(author.photo.path):
                    os.remove(author.photo.path)

    def test_create_author_with_photo(self):
        response = self.client.post(
            self.list_url,
            data=self.valid_data,
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        
        author = Author.objects.first()
        self.assertEqual(author.name, 'Howard Phillips Lovecraft')
        self.assertTrue(author.photo)

    def test_create_author_without_photo(self):
        data = {
            'name': 'George Orwell',
            'birth_date': '1950-01-21'
        }
        
        response = self.client.post(
            self.list_url,
            data=data,
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 1)
        self.assertFalse(Author.objects.first().photo)  # No debería tener foto

    def test_create_author_invalid_data(self):
        response = self.client.post(
            self.list_url,
            data=self.invalid_data,
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Author.objects.count(), 0)

    def test_list_authors(self):
        Author.objects.create(name='Author 1', birth_date='1900-01-01')
        Author.objects.create(name='Author 2', birth_date='1905-01-01')
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_author(self):
        author = Author.objects.create(name='Test Author', birth_date='2000-01-01')
        detail_url = reverse('author-detail', args=[author.id])
        
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')

    def test_update_author(self):
        author = Author.objects.create(name='Old Name', birth_date='2000-01-01')
        detail_url = reverse('author-detail', args=[author.id])
        
        new_image = self.sample_image
        
        update_data = {
            'name': 'New Name',
            'birth_date': '2001-01-01',
            'photo': new_image
        }
        
        response = self.client.put(
            detail_url,
            data=update_data,
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.name, 'New Name')
        self.assertTrue(author.photo)

    def test_delete_author(self):
        author = Author.objects.create(name='To Delete', birth_date='2000-01-01')
        detail_url = reverse('author-detail', args=[author.id])
        
        response = self.client.delete(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)