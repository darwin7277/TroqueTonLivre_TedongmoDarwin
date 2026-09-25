from django.shortcuts import render, redirect
from .forms import RegisterForm, ISBNForm, BookForm, UserForm
from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from .models import Book, User
from .services import get_book_info
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
def accueil(request):
    
    type_filter = request.GET.get('view')

    if type_filter is None:
        type_filter = 'all'

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
    page_number = request.GET.get('page')

    if page_number is None:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    return render(request, 'library/accueil.html', {
        'page_obj': page_obj,
        'vue_courante': type_filter
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

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'library/book_detail.html', {'book':book})

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':

        if book.owner == request.user:
            messages.error(request, "Vous ne pouvez pas réserver votre propre livre.")

        elif not book.is_available:
            messages.error(request, "Ce livre n'est plus disponible.")

        else:
            book.is_available = False
            book.borrower = request.user
            book.save()

            messages.success(request, "Le livre a été réservé avec succès.")

    return redirect('book_detail', book_id=book.id)


@login_required
def return_book(request, book_id):
    book = Book.objects.get(id = book_id)

    if request.method == 'POST':

        if book.owner != request.user:
            messages.error(request, "Vous ne pouvez pas effectuer cette action.")

        elif book.is_available:
            messages.info(request, "Ce livre est déjà disponible.")

        else:
            book.is_available = True
            book.borrower = None
            book.save()

            messages.success(request, "Le livre a été remis.")

    return redirect('book_detail', book_id=book.id)


@login_required
def ajout_book(request):

    isbn_form = ISBNForm()
    book_form = None
    cover_url = ''

    if request.method == 'POST':

        action = request.POST.get('action')

        if action == 'search':
            isbn_form = ISBNForm(request.POST)

            if isbn_form.is_valid():
                isbn = isbn_form.cleaned_data['isbn']
                book_info = get_book_info(isbn)

                if book_info is None:
                    messages.warning(request, "Livre introuvable, saisissez les informations manuellement.")

                    book_form = BookForm(
                        user = request.user,
                        initial = {
                            'isbn': isbn
                        }
                    )

                else:
                    book_form = BookForm(
                        user = request.user,
                        initial = {
                            'isbn': isbn,
                            'title': book_info['title'],
                            'author': book_info['author'],
                            'publisher': book_info['publisher'],
                            'publish_year': book_info['publish_year']
                        }
                    )

                    cover_url = book_info['cover_url']


        elif action == 'save':
            book_form = BookForm(request.POST, user = request.user)

            cover_url = request.POST.get('cover_url')

            if cover_url is None :
                cover_url = ''

            if book_form.is_valid():
                book = book_form.save(commit=False)

                book.owner = request.user
                book.borrower = None
                book.is_available = True
                book.cover_url = cover_url

                book.save()

                messages.success(request, "Le livre a été ajouté avec succès.")

                return redirect('book_detail', book_id=book.id)

            else:
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")


    else:
        if request.GET.get('manual'):
            book_form = BookForm(user = request.user)


    return render(request, 'library/ajout_book.html', {
        'isbn_form': isbn_form,
        'book_form': book_form,
        'cover_url': cover_url,
    })

@login_required
def edit_book(request, book_id):

    book = Book.objects.get(id=book_id)

    if book.owner != request.user:
        messages.error(request, "Vous ne pouvez pas modifier ce livre.")
        return redirect('book_detail', book_id=book.id)


    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():

            isbn = form.cleaned_data['isbn']

            books = Book.objects.filter( isbn=isbn, owner=request.user).exclude(id=book.id)

            if books.exists():
                form.add_error(
                    'isbn',
                    "Vous avez déjà inscrit un ouvrage avec cet ISBN."
                )

            else:
                book.isbn = form.cleaned_data['isbn']
                book.title = form.cleaned_data['title']
                book.author = form.cleaned_data['author']
                book.publisher = form.cleaned_data['publisher']
                book.publish_year = form.cleaned_data['publish_year']
                book.genre = form.cleaned_data['genre']
                book.condition = form.cleaned_data['condition']
                book.comment = form.cleaned_data['comment']

                book.save()

                messages.success(request, "Le livre a été modifié avec succès.")
                return redirect('book_detail', book_id=book.id)

        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")


    else:
        form = BookForm(
            initial={
                'isbn': book.isbn,
                'title': book.title,
                'author': book.author,
                'publisher': book.publisher,
                'publish_year': book.publish_year,
                'genre': book.genre,
                'condition': book.condition,
                'comment': book.comment,
            }
        )


    return render(request, 'library/edit_book.html', {
        'form': form,
        'book': book,
    })


@login_required
def delete_book(request, book_id):

    book = Book.objects.get(id=book_id)

    if book.owner != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer ce livre.")
        return redirect('book_detail', book_id=book.id)


    if request.method == 'POST':
        book.delete()

        messages.success(request, "Le livre a été supprimé avec succès.")
        return redirect('home')


    return redirect('book_detail', book_id=book.id)

@login_required
def profil_pubic(request, pk):
    user = User.objects.get(id=pk)
    books_disponible = Book.objects.filter(owner = user,
                                          is_available = True)
    
    return render(request, 'library/profil_public.html',{
        'user': user,
        'books': books_disponible
    })

@login_required
def profil_prive(request):
    book_user = request.user
    bibliotheque_user = Book.objects.filter(owner=book_user)
    emprunt_user = Book.objects.filter(borrower=book_user)

    return render(request, 'library/profile_prive.html', {
        'bibliotheque_user': bibliotheque_user,
        'emprunt_user': emprunt_user,
        'book_user': book_user
    })

@login_required
def edit_profile(request):

    user = request.user

    if request.method == 'GET':
        form = UserForm(
            initial 
        )


    return render(request, 'library/modif_profil.html')

