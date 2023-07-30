from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Book, BookInstance, Author, Genre, Language


def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_languages = Language.objects.count()

    num_visits = request.session.get("num_visit", 0)
    request.session["num_visit"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_genres": num_genres,
        "num_language": num_languages,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context=context)


class BookListView(ListView):
    model = Book
    paginate_by = 1


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = "catalog/user_borrowed_list.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class AllLoanedList(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = "catalog/all_borrowed_list.html"
    permission_required = "catalog.can_mark_returned"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")
