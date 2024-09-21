from http.client import HTTPResponse

from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    book_objects = Book.objects.all()
    context = {'book_objects': book_objects}
    return render(request, template, context)


def books_view_page(request, pub_date):
    template = 'books/books_list.html'
    book_objects = Book.objects.filter(pub_date=pub_date)
    list_date = list(Book.objects.values_list('pub_date', flat=True).distinct())
    formated_list_date = sorted([date.strftime('%Y-%m-%d') for date in list_date])
    next_date = next_page(formated_list_date, pub_date)
    previous_date = preivous_page(formated_list_date, pub_date)
    context = {'book_objects': book_objects,
               'next_date': next_date,
               'pub_date': pub_date,
               'previous_date': previous_date
               }

    return render(request, template, context)


def next_page(list_date: list, pub_date: str) -> str:
    if pub_date in list_date and \
            list_date.index(pub_date) + 1 < len(list_date) and \
            pub_date[:-3] == list_date[list_date.index(pub_date) + 1][:-3]:
        return list_date[list_date.index(pub_date) + 1]


def preivous_page(list_date: list, pub_date: str) -> str:
    if pub_date in list_date and \
            list_date.index(pub_date) - 1 >= 0 and \
            pub_date[:-3] == list_date[list_date.index(pub_date) - 1][:-3]:
        return list_date[list_date.index(pub_date) - 1]
