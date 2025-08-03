from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>/', views.author_books, name='author_books'),
    path('search/', views.search, name='search'),
    path('api/books/', views.BookListAPIView.as_view(), name='api_books'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
