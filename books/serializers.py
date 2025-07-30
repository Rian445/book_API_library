from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'author_name', 'publication_year']

    def get_author_name(self, obj):
        return obj.authors.first().name if obj.authors.exists() else "Unknown Author"
