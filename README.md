# API Book Collect

A Django-based web application for managing a book collection with REST API functionality. This application allows users to browse books and authors, manage their favorite books, and provides a comprehensive API for accessing book data.

## 🚀 Features

- **Book Management**: Browse and search through a comprehensive book collection
- **Author Profiles**: View detailed author information and their published works
- **User Authentication**: Secure user registration and login system
- **Favorites System**: Authenticated users can manage their favorite books
- **Comments**: Users can post comments on books
- **REST API**: JSON API endpoint for accessing book data
- **Admin Interface**: Django admin panel for data management
- **Responsive Design**: Modern web interface with CSS animations

## 👥 User Roles

- **Anonymous Users**: Browse and search books and authors
- **Authenticated Users**: Manage favorites and post comments
- **Admin Users**: Full access to Django admin interface

## 🏗️ Project Structure

```
Api Book collect/
├── book_collection/          # Main Django project directory
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   └── ...
├── books/                   # Core application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── serializers.py       # API serializers
│   ├── forms.py             # Django forms
│   └── ...
├── templates/               # HTML templates
├── static/                  # CSS, JavaScript, and images
├── manage.py               # Django management script
└── db.sqlite3              # SQLite database
```

## 📊 Database Models

### Author
- `name`: Author's full name
- `birth_date`: Date of birth
- `bio`: Short biography

### Book
- `title`: Book title
- `authors`: Many-to-many relationship with authors
- `cover_image`: URL to book cover
- `publication_year`: Year of publication
- `isbn`: International Standard Book Number
- `description`: Book description
- `open_library_key`: Open Library API key

### Comment
- `book`: Foreign key to Book
- `user`: Foreign key to User
- `content`: Comment text

### Favorite
- `user`: Foreign key to User
- `book`: Foreign key to Book

## 🌐 API Endpoints

### Books API
- **Endpoint**: `/api/books/`
- **Method**: `GET`
- **Description**: Returns a list of all books
- **Format**: JSON

**Example Response:**
```json
[
    {
        "title": "The Lord of the Rings",
        "author_name": "J.R.R. Tolkien",
        "publication_year": "1954"
    }
]
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Django 4.0+
- SQLite (default) or PostgreSQL/MySQL

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository_url>
   cd "Api Book collect"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   pip install djangorestframework
   # Add other dependencies as needed
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Endpoint: http://127.0.0.1:8000/api/books/

## 📱 Main URLs

| URL | Description |
|-----|-------------|
| `/` | Home page with book listings |
| `/book/<id>/` | Book details page |
| `/authors/` | Authors listing |
| `/author/<id>/` | Author's books |
| `/search/` | Search functionality |
| `/register/` | User registration |
| `/login/` | User login |
| `/logout/` | User logout |
| `/dashboard/` | User dashboard |
| `/admin-dashboard/` | Admin overview |
| `/all-books/` | Paginated book list |
| `/api/books/` | REST API endpoint |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues & Support

If you encounter any issues or need support, please create an issue in the repository's issue tracker.
