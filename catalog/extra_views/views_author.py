from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from ..models import Author


class AuthorListView(ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author


class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/author_create.html"


class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = "__all__"
    permission_required = "catalog.can_mark_returned"


class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("authors")
    permission_required = "catalog.can_mark_returned"
