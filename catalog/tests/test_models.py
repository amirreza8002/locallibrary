from django.test import TestCase

from catalog.models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        Author.objects.create(first_name="Big", last_name="Bob")
        cls.author = Author.objects.get(id=1)

    def test_first_Name_label(self):
        field_label = self.author._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_date_of_death_label(self):
        field_label = self.author._meta.get_field("date_of_death").verbose_name
        self.assertEqual(field_label, "died")

    def test_first_name_max_length(self):
        max_length = self.author._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        expected_object_name = f"{self.author.last_name}, {self.author.first_name}"
        self.assertEqual(str(self.author), expected_object_name)

    def test_get_absolutr_url(self):
        self.assertEqual(self.author.get_absolute_url(), "/authors/1")
