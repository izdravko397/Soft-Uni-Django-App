from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Profile, Comment
from .forms import BookForm, CommentForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    books = Book.objects.all()
    user_books = request.user.profile.books.all() if hasattr(request.user, 'profile') else []
    return render(request, 'home.html', {'books': books, 'user_books': user_books})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'inventory.html', {'books': books})

@login_required
def book_create(request):
    if not request.user.is_library_manager:
        return redirect('home')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

@login_required
def book_update(request, pk):
    if not request.user.is_library_manager:
        return redirect('home')
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

@login_required
def book_delete(request, pk):
    if not request.user.is_library_manager:
        return redirect('home')
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})

    
@login_required
def book_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available:
        book.available = False
        book.save()
        # Ensure the user's profile exists and add the book to it
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.books.add(book)
    return redirect('home')


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = book.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = CommentForm()
    return render(request, 'book_detail.html', {'book': book, 'comments': comments, 'form': form})