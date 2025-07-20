import django_filters
from ..models.books import Book

class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='exact')
    
    class Meta: 
        model = Book
        fields = {
            'author__name': ['icontains'],
            'published_year': ['exact', 'gte', 'lte'],
        }