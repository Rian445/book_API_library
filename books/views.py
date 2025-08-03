from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics
from .models import Book, Author, Comment
from .serializers import BookSerializer
from .forms import CustomUserCreationForm, LoginForm, CommentForm


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

    comments = Comment.objects.filter(book=book).select_related('user')

    comment_form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.book = book
                comment.user = request.user
                comment.save()
                messages.success(request, 'Your comment has been added!')
                return redirect('books:book_detail', book_id=book.id)
        else:
            comment_form = CommentForm()

    context = {
        'book': book,
        'related_books': related_books,
        'comments': comments,
        'comment_form': comment_form,
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


def register_view(request):
    if request.user.is_authenticated:
        return redirect('books:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('books:login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'books/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('books:home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'books:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'books/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('books:home')
