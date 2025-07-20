from .author import AuthorSerializer
from ..models.books import Book
from ..models.author import Author
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class BookSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'published_year', 'author', 'author_id', 'is_available']