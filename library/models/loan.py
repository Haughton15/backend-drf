from django.db import models
from .books import Book

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower_name = models.CharField(max_length=100)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.borrower_name} borrowed {self.book.title}"