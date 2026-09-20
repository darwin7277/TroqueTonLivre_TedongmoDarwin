from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField( upload_to='images/', null=True)
    bio = models.TextField(max_length=500 ,blank=True, blank=True)
    city = models.CharField(blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du genre")


class Book(models.Model):
    isbn = models.CharField(verbose_name="ISBN")
    title = models.CharField(verbose_name="Titre")
    author = models.CharField(verbose_name="Autheur")
    publisher = models.CharField(verbose_name="Éditeur", blank=True)
    publish_year = models.IntegerField(verbose_name="Année de publication", blank=True)
    cover_url = models.URLField(verbose_name="Couverture (URL)", blank=True)

    class Condition(models.TextChoices):
        NEUF = 'neuf', 'Neuf'
        T_BON = 'très bon', 'Très bon'
        BON = 'bon', 'Bon'
        USAGE = 'usagé', 'Usagé'

    condition = models.CharField(verbose_name="État", choices=Condition.choices)
    comment = models.CharField(verbose_name="Commentaires du propriétaire", blank=True)
    is_available = models.CharField(verbose_name="Disponible", default=True)
    owner = models.ForeignKey(User, related_name='owned_books', verbose_name='Propriétaire', )
    borrower = models.ForeignKey(User, related_name='borrowed_books', verbose_name="Emprunteur", null=True)
    genre = models.ForeignKey(Genre, related_name='books', verbose_name="Genre")
    
