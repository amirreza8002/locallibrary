from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = "book", "status", "due_back", "borrower"
    list_filter = ("status", "due_back")

    fieldsets = (
        (None, {"fields": ("book", "imprint")}),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )


class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")

    inlines = (BookInstanceInLine,)


class BookInLine(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")

    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    inlines = (BookInLine,)


admin.site.register(Genre)
admin.site.register(Language)
