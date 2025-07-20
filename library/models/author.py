from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    birth_date = models.DateField()
    photo = models.ImageField(upload_to='author/', null=True, blank=True)

    def __str__(self):
        return self.name