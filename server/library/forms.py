from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Book

class BootstrapMixin:
    """Ajoute les classes Bootstrap aux widgets de tous les champs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                css = 'form-check-input'
            elif isinstance(widget, forms.Select):
                css = 'form-select'
            else:
                css = 'form-control'
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = f'{existing} {css}'.strip()

User = get_user_model()

class RegisterForm(BootstrapMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']

class ISBNForm(BootstrapMixin, forms.Form):
    isbn = forms.CharField(  max_length=13, label="ISBN" )

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']

        if not isbn.isdigit() or len(isbn) not in (10, 13):
            raise forms.ValidationError(
                "L'ISBN doit contenir exactement 10 ou 13 caractères numériques."
            )

        return isbn


class BookForm(BootstrapMixin, forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Book

        fields = [
            'isbn',
            'title',
            'author',
            'publisher',
            'publish_year',
            'genre',
            'condition',
            'comment',
        ]

        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4
            }),
        }

        error_messages = {
            'isbn': {
                'required': "L'ISBN est obligatoire."
            },
            'title': {
                'required': "Le titre est obligatoire."
            },
            'author': {
                'required': "L'auteur est obligatoire."
            },
            'condition': {
                'required': "L'état du livre est obligatoire."
            },
        }

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']

        if self.user:
            books = Book.objects.filter(
                isbn=isbn,
                owner=self.user
            )

            if self.instance.pk:
                books = books.exclude(pk=self.instance.pk)

            if books.exists():
                raise forms.ValidationError(
                    "Vous avez déjà inscrit un ouvrage avec cet ISBN."
                )

        return isbn

class UserForm(BootstrapMixin, forms.ModelForm):
      def __init__(self, *args, user=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.user = user
    
      class Meta:
          model = User

      fields = [
                   'username',
                   'nom',
                   'prenom',
                   'city',
                   'bio',
                   'email',
               ]
      
      def clean_user(self):
              
              user = self.cleaned_data['user']

              return self.user
               