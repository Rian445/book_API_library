import requests
import json
from typing import Dict, List, Optional
from .models import Book, Author


class OpenLibraryAPI:
    BASE_URL = "https://openlibrary.org"
    SEARCH_URL = f"{BASE_URL}/search.json"
    COVERS_URL = "https://covers.openlibrary.org/b"

    @classmethod
    def search_books(cls, title: str, limit: int = 5) -> List[Dict]:
        try:
            params = {
                'title': title,
                'limit': limit,
                'fields': 'key,title,author_name,first_publish_year,isbn,cover_i,subject'
            }

            response = requests.get(cls.SEARCH_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return data.get('docs', [])

        except requests.RequestException as e:
            print(f"Error searching books: {e}")
            return []

    @classmethod
    def get_book_details(cls, open_library_key: str) -> Optional[Dict]:
        try:
            url = f"{cls.BASE_URL}{open_library_key}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            print(f"Error getting book details: {e}")
            return None

    @classmethod
    def get_author_details(cls, author_key: str) -> Optional[Dict]:
        try:
            url = f"{cls.BASE_URL}{author_key}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            print(f"Error getting author details: {e}")
            return None

    @classmethod
    def get_cover_url(cls, cover_id: int, size: str = 'M') -> str:
        if cover_id:
            return f"{cls.COVERS_URL}/id/{cover_id}-{size}.jpg"
        return ""

    @classmethod
    def create_book_from_api(cls, book_data: Dict) -> Optional[Book]:
        try:
            title = book_data.get('title', 'Unknown Title')
            open_library_key = book_data.get('key', '')
            publication_year = str(book_data.get('first_publish_year', ''))

            isbn_list = book_data.get('isbn', [])
            isbn = isbn_list[0] if isbn_list else ''

            cover_id = book_data.get('cover_i')
            cover_image = cls.get_cover_url(cover_id) if cover_id else ''

            book = Book.objects.create(
                title=title,
                publication_year=publication_year,
                isbn=isbn,
                cover_image=cover_image,
                open_library_key=open_library_key
            )

            author_names = book_data.get('author_name', [])
            for author_name in author_names:
                author, created = Author.objects.get_or_create(
                    name=author_name,
                    defaults={'bio': f'Author of {title}'}
                )
                book.authors.add(author)

            return book

        except Exception as e:
            print(f"Error creating book from API data: {e}")
            return None


def search_and_create_book(title: str) -> Optional[Book]:
    books_data = OpenLibraryAPI.search_books(title, limit=1)

    if not books_data:
        return None

    book_data = books_data[0]

    open_library_key = book_data.get('key', '')
    if open_library_key:
        existing_book = Book.objects.filter(open_library_key=open_library_key).first()
        if existing_book:
            return existing_book

    return OpenLibraryAPI.create_book_from_api(book_data)
