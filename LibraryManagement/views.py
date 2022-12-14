from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import AddBook
from .models import Book


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('showBooks')
    else:
        form = AuthenticationForm()
    return render(request, 'LibraryManagement/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'LibraryManagement/ShowBooks.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'LibraryManagement/register.html', {'form': form})


@login_required(login_url='login')
def addBook(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = AddBook(request.POST, request.FILES)  # request.FILES is added for the image field
        # check whether it's valid:
        if form.is_valid():
            # Assign the current user as the user (i.e., owner) for each task
            form.instance.user = request.user
            # save the record into the db
            form.save()
            # after saving redirect to index page
            return redirect('showBooks')
    else:
        # if the request does not have post data, a blank form will be rendered
        form = AddBook()

    return render(request, 'LibraryManagement/AddBook.html', {'form': form})


@login_required(login_url='login')
def showBooks(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'LibraryManagement/ShowBooks.html', context)


@login_required(login_url='login')
def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    form = AddBook(request.POST or None, instance=book)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('showBooks')
    context = {'form': form}
    return render(request, 'LibraryManagement/updateBook.html', context)


def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('showBooks')


def search(request):
    if request.method == "GET":
        search_term = request.GET.get('search') or ''
        books = Book.objects.filter(bookName__icontains=search_term)
        context = {'books': books}
        return render(request, 'LibraryManagement/ShowBooks.html', context)


def issue(request, book_id, returned):
    rent_book = Book.objects.get(id=book_id, user=request.user)
    if returned == 0:
        rent_book.rented = True
    elif returned == 1:
        rent_book.rented = False
    rent_book.user = request.user
    rent_book.save()
    return redirect('showBooks')
