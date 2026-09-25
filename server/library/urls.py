from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='home'),
    path('signup/', views.signup, name='signup'),
    path('book/<int:book_id>', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/reserve/', views.reserve_book, name='reserve_book'),
    path('book/<int:book_id>/return/', views.return_book, name='return_book' ),
    path('book/ajouter', views.ajout_book, name='ajout_book'),
    path('book/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', views.delete_book, name='delete_book' ),
]   
