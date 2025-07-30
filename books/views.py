from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from rest_framework import generics
from .models import Book, Author
from .serializers import BookSerializer


def home(request):
    books_list = Book.objects.all().prefetch_related('authors')

    paginator = Paginator(books_list, 10)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    total_books = Book.objects.count()
    total_authors = Author.objects.count()

    latest_book = Book.objects.filter(publication_year__isnull=False).order_by('-publication_year').first()
    latest_year = latest_book.publication_year if latest_book else 'N/A'

    context = {
        'books': books,
        'total_books': total_books,
        'total_authors': total_authors,
        'latest_year': latest_year,
        'is_paginated': books.has_other_pages(),
        'page_obj': books,
    }

    return render(request, 'books/home.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    related_books = Book.objects.filter(
        authors__in=book.authors.all()
    ).exclude(id=book.id).distinct()[:4]

    context = {
        'book': book,
        'related_books': related_books,
    }

    return render(request, 'books/book_detail.html', context)


def authors(request):
    authors_list = Author.objects.annotate(
        book_count=Count('books')
    ).filter(book_count__gt=0).order_by('name')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        authors_list = authors_list.filter(
            name__icontains=search_query
        )

    paginator = Paginator(authors_list, 12)
    page_number = request.GET.get('page')
    authors_page = paginator.get_page(page_number)

    context = {
        'authors': authors_page,
        'search_query': search_query,
        'is_paginated': authors_page.has_other_pages(),
        'page_obj': authors_page,
    }

    return render(request, 'books/authors.html', context)


def author_books(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    books_list = author.books.all().order_by('-created_at')

    paginator = Paginator(books_list, 12)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    context = {
        'author': author,
        'books': books,
        'is_paginated': books.has_other_pages(),
        'page_obj': books,
    }

    return render(request, 'books/author_books.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.none()
    authors = Author.objects.none()

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(authors__name__icontains=query)
        ).distinct().prefetch_related('authors')

        authors = Author.objects.filter(
            name__icontains=query
        ).annotate(book_count=Count('books')).filter(book_count__gt=0)

    context = {
        'query': query,
        'books': books,
        'authors': authors,
    }

    return render(request, 'books/search.html', context)


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all().prefetch_related('authors')
    serializer_class = BookSerializer
