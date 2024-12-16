from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from .validators import validate_published_date, validate_isbn

class CustomUser(AbstractUser):
    is_library_manager = models.BooleanField(default=False)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(validators=[validate_published_date])
    isbn = models.CharField(max_length=13,
     unique=True,
     help_text='13 digits',
     validators=[validate_isbn],
     )
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.book.title}'