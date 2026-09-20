from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Genre, Book

@admin.register(User)
class Utilisateur(UserAdmin):
    list_display = (
        'username', 'email', 'city',
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'isbn', 'title', 'author', 'genre', 'condition', 'owner',
        'borrower', 'is_available',
    )

    list_filter = (
        'genre', 'condition',
    )

    search_fields = (
        'title', 'author', 'isbn',
    )