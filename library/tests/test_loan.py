# library/tests/test_loans.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from ..models.loan import Loan
from ..models.books import Book
from ..models.author import Author

class LoanViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('loan-list')
        
        self.author = Author.objects.create(
            name='Test Author',
            birth_date='2000-01-01',
            photo=None 
        )

        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            published_year='2023-01-01',
            is_available=True
        )

        self.loan_data = {
            'book': self.book.id,
            'borrower_name': 'Test Borrower'
        }

    def create_loan(self, returned=False):
        loan = Loan.objects.create(
            book=self.book,
            borrower_name='Test Borrower'
        )
        
        if returned:
            loan.return_date = timezone.now().date()
            loan.save()
            self.book.is_available = True
            self.book.save()
        else:
            self.book.is_available = False
            self.book.save()
        return loan

    def test_create_loan(self):
        response = self.client.post(
            self.list_url,
            data=self.loan_data,
            format='json'
        )

        self.book.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)
        self.assertFalse(self.book.is_available)

    def test_list_loans(self):
        self.create_loan()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_loan(self):
        loan = self.create_loan()
        detail_url = reverse('loan-detail', args=[loan.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['borrower_name'], 'Test Borrower')

    def test_return_loan_success(self):
        loan = self.create_loan()
        return_url = reverse('loan-return-loan', args=[loan.id])
        
        response = self.client.post(return_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        loan.refresh_from_db()
        self.assertIsNotNone(loan.return_date)
        self.assertEqual(loan.return_date, timezone.now().date())
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_available)

    def test_return_already_returned_loan(self):
        loan = self.create_loan(returned=True)
        return_url = reverse('loan-return-loan', args=[loan.id])
        
        response = self.client.post(return_url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'El préstamo ya ha sido devuelto')
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_available)

    def test_loan_a_book_not_available(self):
        self.book.is_available = False
        self.book.save()
        
        response = self.client.post(
            self.list_url,
            data=self.loan_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('El libro no está disponible para préstamo.', str(response.data))

    def test_return_nonexistent_loan(self):
        return_url = reverse('loan-return-loan', args=[999]) 
        response = self.client.post(return_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_loan_dates(self):
        loan = self.create_loan()
        self.assertIsNone(loan.return_date)
        self.assertEqual(loan.loan_date, timezone.now().date())