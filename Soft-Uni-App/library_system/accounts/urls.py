from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('inventory/', views.book_list, name='book_list'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/update/<int:pk>/', views.book_update, name='book_update'),
    path('book/delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('book/book/<int:pk>/', views.book_book, name='book_book'),
]