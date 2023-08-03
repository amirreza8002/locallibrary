from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

from .models import Book, BookInstance, Author, Genre, Language, Author
from .forms import RenewBookForm

from .extra_views.views_author import *
from .extra_views.views_book import *

import datetime


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


@login_required
@permission_required("catalog.can_mark_returned", raise_exception=True)
def renew_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data["due_back"]
            book_instance.save()

            return HttpResponseRedirect(reverse("borrowed_books"))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={"due_back": proposed_renewal_date})

    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/renew_book.html", context)


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
