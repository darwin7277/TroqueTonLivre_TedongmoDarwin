from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login

# Create your views here.
def accueil(request):
    return render(request, 'library/accueil.html')

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