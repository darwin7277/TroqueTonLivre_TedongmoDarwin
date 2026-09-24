from django.db import models
from datetime import date
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import ( MinLengthValidator,MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
# Create your models here.



class User(AbstractUser):
    avatar = models.ImageField( upload_to='images/', null=True)
    bio = models.TextField(max_length=500, blank=True)
    city = models.CharField(blank=True)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["username"]
    
    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du genre")

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    isbn = models.CharField(verbose_name="ISBN", max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\d{10}(\d{3})?$',
                message="L'ISBN doit contenir exactement 10 ou 13 caractères numériques."
            )
        ])
    title = models.CharField(max_length=200,verbose_name="Titre",
        validators=[
            MinLengthValidator(
                2,
                "Le titre doit contenir au moins 2 caractères"
            )
        ])
    author = models.CharField(max_length=150 ,verbose_name="Autheur", 
            validators=[
                MinLengthValidator(
                    2,
                    "Le nom de l'auteur doit contenir au moins 2 caractères."
                )
            ])
    publisher = models.CharField(verbose_name="Éditeur", blank=True)
    publish_year = models.IntegerField(verbose_name="Année de publication", blank=True,
            validators=[
                MinValueValidator(1450),
                MaxValueValidator(date.today().year)
            ])
    cover_url = models.URLField(verbose_name="Couverture (URL)", blank=True)

    class Condition(models.TextChoices):
        NEUF = 'neuf', 'Neuf'
        T_BON = 'très bon', 'Très bon'
        BON = 'bon', 'Bon'
        USAGE = 'usagé', 'Usagé'

    condition = models.CharField(verbose_name="État", choices=Condition.choices)

    comment = models.CharField(verbose_name="Commentaires du propriétaire", blank=True, validators=[
        MinLengthValidator(
            10,
            "Le commentaire doit contenir au moins 10 caractères.")
    ])

    is_available = models.BooleanField(verbose_name="Disponible", default=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_books', 
                verbose_name='Propriétaire', 
                on_delete = models.CASCADE
            )
    
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='borrowed_books',
            verbose_name="Emprunteur",
            null=True,
            blank=True,
            on_delete= models.SET_NULL)

    genre = models.ForeignKey(Genre, related_name='books',
             null= True,
             verbose_name="Genre",
             on_delete= models.SET_NULL
             )

    class Meta:
        verbose_name = "Ouvrage"
        verbose_name_plural = "Ouvrages"
        ordering = ["title"]

        constraints = [
            models.UniqueConstraint(
                fields=['isbn', 'owner'],
                name = 'unique_isbn_per_owner',
                violation_error_message = "Un membre ne peut pas inscrire deux fois le même livre."
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(is_available=True, borrower__isnull=True)|
                    models.Q(is_available=False, borrower__isnull=False)
                ),
                name='valid_book_reservation',
                violation_error_message="Un ouvrage disponible ne peut pas avoir d'emprunteur"
            )
            
        ]

    def __str__(self):
        return self.title
