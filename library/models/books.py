from django.db import models
from .author import Author

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_year = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
