from django.shortcuts import render
from django.views import generic
from books.models import Book

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/books_list.html'

    def get_queryset(self):
        if self.kwargs:
            return Book.objects.filter(pub_date=self.kwargs['pub_date'])
        else:
            return Book.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs:
            previous_book = Book.objects.filter(pub_date__lt=self.kwargs['pub_date']).order_by('-pub_date')
            if previous_book.exists():
                previous_date = str(previous_book[0].pub_date)
                context['prev_date'] = previous_date
            next_book = Book.objects.filter(pub_date__gt=self.kwargs['pub_date']).order_by('pub_date')
            if next_book.exists():
                next_date = str(next_book[0].pub_date)
                context['next_date'] = next_date
        return context
