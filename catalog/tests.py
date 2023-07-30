from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Book, Author, Language, Genre, BookInstance
import datetime


class BookTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="testpass123",
        )

        self.language = Language.objects.create(language="English")

        self.genre = Genre.objects.create(name="Drama")

        self.author = Author.objects.create(
            first_name="Jane",
            last_name="Austen",
            date_of_birth=datetime.date(1775, 12, 16),
            date_of_death=datetime.date(1817, 7, 18),
        )

        self.book = Book.objects.create(
            title="Pride and prejudice",
            author=self.author,
            summary="good novel",
            isbn="3214567890432",
        )
        self.all_genre = Genre.objects.all()
        self.book.genre.set(self.all_genre)

        self.all_language = Language.objects.all()
        self.book.language.set(self.all_language)

        self.book.save()

        self.bookinstance = BookInstance.objects.create(
            book=self.book, imprint="2", due_back=datetime.date(2023, 12, 5), status="a"
        )

    def test_language(self):
        self.assertEqual(f"{self.language.language}", "English")

    def test_genre(self):
        self.assertEqual(f"{self.genre.name}", "Drama")

    def test_author_info(self):
        self.assertEqual(f"{self.author.first_name}", "Jane")
        self.assertEqual(f"{self.author.last_name}", "Austen")
        self.assertEqual(self.author.date_of_birth, datetime.date(1775, 12, 16))
        self.assertEqual(self.author.date_of_death, datetime.date(1817, 7, 18))

    def test_book_listing(self):
        self.assertEqual(f"{self.book.title}", "Pride and prejudice")
        self.assertEqual(f"{self.book.author}", "Austen, Jane")

        self.assertEqual(f"{self.book.isbn}", "3214567890432")
        self.assertEqual(self.book.summary, "good novel")

        self.assertListEqual([str(genre) for genre in self.book.genre.all()], ["Drama"])
        self.assertListEqual(
            [str(language) for language in self.book.language.all()], ["English"]
        )

    def test_book_instance(self):
        self.assertEqual(f"{self.bookinstance.book}", "Pride and prejudice")
        self.assertEqual(f"{self.bookinstance.imprint}", "2")
        self.assertEqual(self.bookinstance.due_back, datetime.date(2023, 12, 5))
        self.assertEqual(f"{self.bookinstance.status}", "a")
