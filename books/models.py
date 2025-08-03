from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    birth_date = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:author_books', kwargs={'author_id': self.pk})


class Book(models.Model):
    title = models.CharField(max_length=300)
    authors = models.ManyToManyField(Author, related_name='books')
    cover_image = models.URLField(blank=True, null=True)
    publication_year = models.CharField(max_length=10, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    open_library_key = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'book_id': self.pk})

    def get_authors_display(self):
        return ", ".join([author.name for author in self.authors.all()])

    def get_cover_url(self):
        if self.cover_image:
            return self.cover_image
        return '/static/images/no-cover.jpg'


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.book.title}'
