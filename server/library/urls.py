from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='home'),
    path('signup/', views.signup, name='signup')
]
