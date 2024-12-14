from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Profile, Comment
from .forms import BookForm, CommentForm
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


def index_view(request):
    return render(request, 'index.html')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class LoginView(View):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})



class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            context['books'] = Book.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query)
            )
        else:
            context['books'] = Book.objects.all()
        context['user_books'] = self.request.user.profile.books.all() if hasattr(self.request.user, 'profile') else []
        return context


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home')


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'inventory.html'
    context_object_name = 'books'

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


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = self.object
            comment.save()
            return redirect('book_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def book_return(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Logic to mark the book as returned
        book.available = True
        book.save()
        # Optionally, remove the book from the user's profile if needed
        # request.user.profile.books.remove(book)
    return redirect('profile')