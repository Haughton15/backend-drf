from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models.books import Book
from ..models.author import Author
import datetime

class BookViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            name="Test Author",
            birth_date="2000-01-01"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            published_year="2023-01-01"
        )
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book.id])

    def test_get_all_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Book")

    def test_get_single_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book")

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author_id": self.author.id,
            "published_year": "2024-01-01",
            "is_available": True
        }
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "author_id": self.author.id,
            "published_year": "2023-01-01",
            "is_available": True
        }
        response = self.client.put(self.detail_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

class BookFilterTest(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name="Author 1", birth_date="2000-01-01")
        self.author2 = Author.objects.create(name="Author 2", birth_date="2000-01-01")
        
        self.book1 = Book.objects.create(
            title="Book 1",
            author=self.author1,
            published_year="2020-01-01"
        )
        self.book2 = Book.objects.create(
            title="Book 2",
            author=self.author2,
            published_year="2023-01-01"
        )
        self.book3 = Book.objects.create(
            title="Book 3",
            author=self.author1,
            published_year="2021-01-01"
        )

    def test_filter_by_author_name(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?author=Author 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Book 1")
        self.assertEqual(response.data[1]['title'], "Book 3")

    def test_filter_by_author_name_icontains(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?author__name__icontains=thor")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_published_year_exact(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?published_year=2020-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book 1")

    def test_filter_by_published_year_gte(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?published_year__gte=2021-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_published_year_lte(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?published_year__lte=2021-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)