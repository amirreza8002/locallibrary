from django.urls import path

from .views import (
    index,
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView,
    LoanedBooksByUserListView,
    AllLoanedList,
)

urlpatterns = [
    path("", index, name="index"),
    path("book/", BookListView.as_view(), name="books"),
    path("book/<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
    path("authors/", AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author_detail"),
    path("mybooks/", LoanedBooksByUserListView.as_view(), name="my_books"),
    path("borrowed_books/", AllLoanedList.as_view(), name="borrowed_books"),
]
