from django.urls import path

from .views import (
    index,
    renew_book,
    LoanedBooksByUserListView,
    AllLoanedList,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    AuthorListView,
    AuthorDetailView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("mybooks/", LoanedBooksByUserListView.as_view(), name="my_books"),
    path("borrowed_books/", AllLoanedList.as_view(), name="borrowed_books"),
    path("renew_book/<uuid:pk>/", renew_book, name="renew_book"),
]

urlpatterns += [
    path("book/", BookListView.as_view(), name="books"),
    path("book/<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
    path("book/create/", BookCreateView.as_view(), name="book_create"),
    path("book/<uuid:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("book/<uuid:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
]


urlpatterns += [
    path("authors/", AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author_detail"),
    path("authors/create/", AuthorCreateView.as_view(), name="author_create"),
    path("authors/<int:pk>/update/", AuthorUpdateView.as_view(), name="author_update"),
    path("authors/<int:pk>/delete/", AuthorDeleteView.as_view(), name="author_delete"),
]
