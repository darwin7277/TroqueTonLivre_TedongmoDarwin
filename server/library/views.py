from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from .models import Book

# Create your views here.
def accueil(request):

    type_filter = request.GET.get('view', 'all')

    books = Book.objects.all()

    if request.user.is_authenticated:

        if type_filter == 'library':
            books = Book.objects.filter(
                owner = request.user
            )

        elif type_filter == 'emprunt':
            books = Book.objects.filter(
                borrower = request.user
            )

    else:
        type_filter = 'all'
        
    paginator = Paginator(books,6)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    

    return render(request, 'library/accueil.html', {
        'page_obj': page_obj,
        'vue_courante': type_filter,
    })

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succèss')
            return redirect('home')

        else:
            messages.error(request, "Veuillez corriger les érreurs ci dessous")
    else:
        form = RegisterForm()


    return render(request, 'library/signup.html', {'form':form})