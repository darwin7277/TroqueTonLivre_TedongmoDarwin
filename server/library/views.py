from django.shortcuts import render

# Create your views here.
def accueil(request):
    return render(request, 'library/accueil.html')

def signup(request):
    return render(request, 'library/signup.html')