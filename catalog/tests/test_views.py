from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from catalog.models import Author, Book, BookInstance, Genre, Language

import datetime
import uuid


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f"John {author_id}",
                last_name=f"smit {author_id}",
            )

    def test_view_url_exists_at_location(self):
        response = self.client.get("/authors/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code, 200)

    def test_view_correct_template(self):
        response = self.client.get(reverse("authors"))
        self.assertTemplateUsed(response, "catalog/author_list.html")

    def test_pagination_is_ten(self):
        response = self.client.get(reverse("authors"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["author_list"]), 10)

    def test_lists_all_authors(self):
        response = self.client.get(f"{reverse('authors')}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["author_list"]), 3)


class LoanedBookInstanceByUserListViewTest(TestCase):
    def setUp(self) -> None:
        test_user1 = get_user_model().objects.create_user(
            username="testuser1",
            password="testpass123",
            email="testuser1@email.com",
        )
        test_user2 = get_user_model().objects.create_user(
            username="testuser2",
            password="testpass123",
            email="testuser2@email.com",
        )

        test_user1.save()
        test_user2.save()

        test_author = Author.objects.create(first_name="John", last_name="Smith")
        test_genre = Genre.objects.create(name="Fantasy")
        test_language = Language.objects.create(language="English")
        test_book = Book.objects.create(
            title="Book Title",
            summary="My Book summary",
            isbn="ABCDEFG",
            author=test_author,
        )

        genre_objects_for_books = Genre.objects.all()
        language_objects_for_books = Language.objects.all()
        test_book.genre.set(genre_objects_for_books)
        test_book.language.set(language_objects_for_books)
        test_book.save()

        number_of_copies = 30

        for book_copy in range(number_of_copies):
            return_date = timezone.localtime() + datetime.timedelta(days=book_copy % 5)
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = "m"
            BookInstance.objects.create(
                book=test_book,
                imprint="Unlikely Imprint, 2016",
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("my_books"))
        self.assertRedirects(
            response, "/accounts/password/reset/login/?next=%2Fmybooks%2F"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email="testuser1@email.com", password="testpass123")
        response = self.client.get(reverse("my_books"))

        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/user_borrowed_list.html")

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(email="testuser1@email.com", password="testpass123")
        response = self.client.get(reverse("my_books"))

        self.assertTrue("bookinstance_list" in response.context)
        self.assertEqual(len(response.context["bookinstance_list"]), 0)

        books = BookInstance.objects.all()[:10]
        for book in books:
            book.status = "o"
            book.save()

        response = self.client.get(reverse("my_books"))

        for bookitem in response.context["bookinstance_list"]:
            self.assertEqual(response.context["user"], bookitem.borrower)
            self.assertEqual(bookitem.status, "o")

    def test_pages_ordered_by_due_back(self):
        for book in BookInstance.objects.all():
            book.status = "o"
            book.save()

        login = self.client.login(email="testuser1@email.com", password="testpass123")
        response = self.client.get(reverse("my_books"))

        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["bookinstance_list"]), 10)

        last_date = 0
        for book in response.context["bookinstance_list"]:
            if last_date == 0:
                last_date = book.due_back
            else:
                self.assertTrue(last_date <= book.due_back)
                last_date = book.due_back


class RenewBookInstanceViewTest(TestCase):
    def setUp(self):
        test_user1 = get_user_model().objects.create_user(
            username="testuser1", email="testuser1@email.com", password="testpass123"
        )
        test_user2 = get_user_model().objects.create_user(
            username="testuser2", email="testuser2@email.com", password="testpass123"
        )
        permission = Permission.objects.get(codename="can_mark_returned")
        test_user2.user_permissions.add(permission)

        test_author = Author.objects.create(first_name="John", last_name="Smith")
        test_genre = Genre.objects.create(name="Fantasy")
        test_language = Language.objects.create(language="English")
        test_book = Book.objects.create(
            title="book title",
            summary="book summary",
            isbn="isbntest",
            author=test_author,
        )
        genre_objects_for_book = Genre.objects.all()
        language_objects_for_book = Language.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.language.set(language_objects_for_book)
        test_book.save()

        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint="Unlikely imprint, 976",
            due_back=return_date,
            borrower=test_user1,
            status="o",
        )

        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint="Unliekly imprint, 856",
            due_back=return_date,
            borrower=test_user2,
            status="o",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("renew_book", kwargs={"pk": self.test_bookinstance1.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/password/reset/login/"))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(email="testuser1@email.com", password="testpass123")
        response = self.client.get(
            reverse("renew_book", kwargs={"pk": self.test_bookinstance1.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(email="testuser2@email.com", password="testpass123")
        response = self.client.get(
            reverse("renew_book", kwargs={"pk": self.test_bookinstance2.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        test_uid = uuid.uuid4()
        login = self.client.login(email="testuser2@email.com", password="testpass123")
        response = self.client.get(reverse("renew_book", kwargs={"pk": test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(email="testuser2@email.com", password="testpass123")
        response = self.client.get(
            reverse("renew_book", kwargs={"pk": self.test_bookinstance1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/renew_book.html")

    def test_form_renewal_date_initial_value(self):
        login = self.client.login(email="testuser2@email.com", password="testpass123")
        response = self.client.get(
            reverse("renew_book", kwargs={"pk": self.test_bookinstance1.pk})
        )

        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)

        self.assertEqual(
            response.context["form"].initial["due_back"], date_3_weeks_in_future
        )

    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(email="testuser2@email.com", password="testpass123")
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)

        response = self.client.post(
            reverse("renew_book", kwargs={"pk": self.test_bookinstance1.pk}),
            {"due_back": valid_date_in_future},
        )

        self.assertRedirects(response, reverse("borrowed_books"))

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(email="testuser2@email.com", password="testpass123")
        date_in_past = datetime.date.today() - datetime.timedelta(days=1)

        response = self.client.post(
            reverse("renew_book", kwargs={"pk": self.test_bookinstance1.pk}),
            {"due_back": date_in_past},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "due_back", "Invalid date - renewal in past"
        )

    def test_from_invalid_renewal_date_in_future(self):
        login = self.client.login(email="testuser2@email.com", password="testpass123")
        date_in_future = datetime.date.today() + datetime.timedelta(weeks=4, days=1)

        response = self.client.post(
            reverse("renew_book", kwargs={"pk": self.test_bookinstance1.pk}),
            {"due_back": date_in_future},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "due_back",
            "Invalid date - renewal more than 4 weeks ahead",
        )


class AuthorCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = get_user_model().objects.create_user(
            username="testuser1",
            email="testuser1@email.com",
            password="testpass123",
        )
        cls.test_user2 = get_user_model().objects.create_user(
            username="testuser2",
            email="testuser2@email.com",
            password="testpass123",
        )

        cls.special_permission = Permission.objects.get(codename="can_mark_returned")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("author_create"))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/password/reset/login"))
        self.assertRedirects(response, "%s?next=/authors/create/" % (reverse("account_login")))

    def test_forbidden_if_logged_in_but_no_permission(self):
        self.client.login(email="testuser1@email.com", password="testpass123")
        response = self.client.get(reverse("author_create"))

        self.assertEqual(response.status_code, 403)

    def test_access_if_logged_in_with_permission(self):
        self.client.login(email="testuser2@email.com", password="testpass123")
        response = self.client.get(reverse("author_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/author_create.html")
