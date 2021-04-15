from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from books.models import Author, Book, Genre


def index(request):
    return render(request, 'base.html')


def detail_author_view(request, id):
    author = Author.objects.get(pk=id)
    return render(request, 'author_detail_view.html', {'author': author})


def detail_book_view(request, id):
    book = Book.objects.get(pk=id)
    return render(request, 'book_detail_view.html', {'book': book})


def authors_view(request):
    # authors = Author.objects.all()
    nazwisko = request.GET.get('nazwisko', '')  # woj
    imie = request.GET.get('imie', '')
    authors = Author.objects.filter(last_name__icontains=nazwisko)
    authors = authors.filter(first_name__icontains=imie)
    return render(request, 'autor_list.html', {'object_list': authors, "s": request.session})


def books_view(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'object_list': books})


def author_add_view(request):
    if request.method == 'GET':
        return render(request, 'add_author.html')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    year = request.POST.get('year')
    a = Author(first_name=first_name, last_name=last_name, year=year)
    a.save()
    return render(request, 'add_author.html')


def create_session(request):
    if request.method == 'GET':
        return render(request, 'show_session.html')
    key = request.POST['key']
    val = request.POST['value']
    request.session[key] = val
    z = f"""
    <table>
    <tr><td>a</td><td>a</td><td>a</td><td>a</td><td>a</td></tr>
    <tr><td>a</td><td>a</td><td>a</td><td>a</td><td>a</td></tr>
    <tr><td>a</td><td>a</td><td>a</td><td>a</td><td>a</td></tr>
    <tr><td>a</td><td>a</td><td>a</td><td>a</td><td>a</td></tr>
    </table>
    Jupikajej udało sie dodać do sesj {request.session.values()}
    """
    return HttpResponse(z)


def show_session_all(request):
    return render(request, 'blebleble.html', {"sessions": request.session})


def create_cookies(request):
    if request.method == 'GET':
        return render(request, 'show_session.html', {"sessions": request.COOKIES})
    key = request.POST['key']
    val = request.POST['value']
    httpResponse = render(request, 'show_session.html', {"sessions": request.COOKIES})
    httpResponse.set_cookie(key, val)
    return httpResponse


def set_session(request):
    request.session['counter'] = 0
    return render(request, 'set_session.html')


def show_session(request):
    try:
        request.session['counter'] += 1
        counter = request.session['counter']
    except:
        counter = 0
    return render(request, 'show2_session.html', {'counter': counter})


def del_session(request):
    try:
        del request.session['counter']
        return render(request, 'del_session.html', {'msg': 'udało sie skasować'})
    except:
        return render(request, 'del_session.html', {'msg': "nie udało sie skasowas bo nie było"})


def login(request):
    if request.method == 'GET':
        swinka = request.session.get('loggedUser', '')
        return render(request, 'login.html', {'logged': swinka})
    elif request.method == 'POST':
        name = request.POST['homogeniczny']
        request.session['loggedUser'] = name

        return render(request, 'login.html', {"logged": name})


def book_add_view(request):
    authors = Author.objects.all()
    genres = Genre.objects.all()
    if request.method == 'GET':
        return render(request, 'add_book.html', {'authors': authors, 'genres': genres})
    title = request.POST.get('title')
    author_id = request.POST.get('author_id')
    autor = Author.objects.get(id=author_id)
    b = Book(title=title, author=autor)
    b.save()
    gatunki = request.POST.getlist('genre')
    b.categories.set(gatunki)
    return render(request, 'add_book.html', {'authors': authors, 'genres': genres})


class AddBookView(View):

    def get(self, request):
        authors = Author.objects.all()
        genres = Genre.objects.all()
        return render(request, 'add_book.html', {'authors': authors, 'genres': genres})

    def post(self, request):
        authors = Author.objects.all()
        genres = Genre.objects.all()
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        autor = Author.objects.get(id=author_id)
        b = Book(title=title, author=autor)
        b.save()
        gatunki = request.POST.getlist('genre')
        b.categories.set(gatunki)
        return render(request, 'add_book.html', {'authors': authors, 'genres': genres})


class BooksView(View):

    def get(self, request):
        books = Book.objects.all()
        return render(request, 'book_list.html', {'object_list': books})


class DetailBookView(View):
    def get(self, request, id):
        book = Book.objects.get(pk=id)
        return render(request, 'book_detail_view.html', {'book': book})

