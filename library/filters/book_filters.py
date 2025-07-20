import django_filters
from ..models.books import Book

class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'author': ['exact'],
            'published_year': ['exact', 'gte', 'lte'],
        }