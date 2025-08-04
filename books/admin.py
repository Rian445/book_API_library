from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Book, Author, Comment, Favorite
from .utils import search_and_create_book, OpenLibraryAPI


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    readonly_fields = ('created_at',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors_display', 'publication_year', 'created_at')
    list_filter = ('publication_year', 'created_at', 'authors')
    search_fields = ('title', 'authors__name', 'isbn')
    filter_horizontal = ('authors',)
    readonly_fields = ('created_at', 'updated_at', 'open_library_key')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-from-api/', self.add_from_api_view, name='books_book_add_from_api'),
        ]
        return custom_urls + urls

    def add_from_api_view(self, request):
        if request.method == 'POST':
            book_title = request.POST.get('book_title', '').strip()

            if not book_title:
                messages.error(request, 'Please enter a book title.')
                return render(request, 'admin/books/add_from_api.html')

            book = search_and_create_book(book_title)

            if book:
                messages.success(
                    request,
                    f'Book "{book.title}" has been successfully added to the database.'
                )
                return HttpResponseRedirect(f'/admin/books/book/{book.id}/change/')
            else:
                messages.error(
                    request,
                    f'Could not find book "{book_title}" in Open Library. Please try a different title.'
                )

        return render(request, 'admin/books/add_from_api.html')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_from_api_url'] = 'add-from-api/'
        return super().changelist_view(request, extra_context=extra_context)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'content_preview', 'created_at')
    list_filter = ('created_at', 'book')
    search_fields = ('user__username', 'user__first_name', 'book__title', 'content')
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Comment Preview'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'book__title')
    readonly_fields = ('created_at',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavoriteAdmin)

admin.site.site_header = "Book Collection Admin"
admin.site.site_title = "Book Collection"
admin.site.index_title = "Welcome to Book Collection Administration"
