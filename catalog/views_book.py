from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Book


class BookListView(ListView):
    model = Book
    paginate_by = 1


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book


class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    fields = [
        "title",
        "author",
        "summary",
        "isbn",
        "genre",
        "language",
    ]


class BookUpdateView(UpdateView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    fields = [
        "title",
        "author",
        "summary",
        "isbn",
        "genre",
        "language",
    ]


class BookDeleteView(DeleteView):
    model = Book
    permission_required = "catalog.can_mark_returned"
    success_url = reverse_lazy("books")
