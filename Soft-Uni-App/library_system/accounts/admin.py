from django.contrib import admin
from .models import Book, Profile, Comment

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn', 'available')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('available', 'published_date')
    ordering = ('title',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'books__title')
    search_fields = ('user__username',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at')
    search_fields = ('user__username', 'book__title')
    list_filter = ('rating', 'created_at')



admin.site.site_header = "Library System Admin"
admin.site.site_title = "Library System Admin Portal"
admin.site.index_title = "Welcome to the Library System Admin"