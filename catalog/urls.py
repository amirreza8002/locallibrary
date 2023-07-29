from django.urls import path

from .views import index, BookListView, BookDetailView, AuthorListView, AuthorDetailView

urlpatterns = [
    path("", index, name="index"),
    path("book/", BookListView.as_view(), name="books"),
    path("book/<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
    path("authors/", AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author_detail"),
]
