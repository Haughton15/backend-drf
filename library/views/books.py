from rest_framework.viewsets import ModelViewSet
from ..models.books import Book
from ..serializers.books import BookSerializer
from ..filters.book_filters import BookFilter

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
