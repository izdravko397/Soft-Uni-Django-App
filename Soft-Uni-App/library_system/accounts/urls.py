from django.urls import path
from . import views
from .views import RegisterView, LoginView, HomeView, BookListView, BookDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('index/', views.index_view, name='index'),
    path('profile/', views.profile, name='profile'),
    path('inventory/', BookListView.as_view(), name='book_list'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/update/<int:pk>/', views.book_update, name='book_update'),
    path('book/delete/<int:pk>/', views.book_delete, name='book_delete'),
    path('book/book/<int:pk>/', views.book_book, name='book_book'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/return/<int:pk>/', views.book_return, name='book_return'),
]