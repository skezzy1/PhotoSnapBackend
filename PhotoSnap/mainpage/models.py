from django.db import models
from accounts.models import BaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class BookManager(models.Manager):
    def create_book(self, user, name, author, book_type, book_category):
        book = self.model(
            user=user,
            name=name,
            author=author,
            book_type=book_type,
            book_category=book_category,
        )
        book.save(using=self._db)
        return book

class Book(models.Model):
    def bookFile(instance, filename):
        return '/'.join(['products', str(instance.id), filename])

    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)  # Зміна поля book_name на name
    author = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=bookFile, blank=True, null=True)  # Додано поле для зображення
    book_time_created = models.DateTimeField(verbose_name=_('Date creation'), default=timezone.now)

    book_type_choice = [
        (-1, 'Select type'),
        (1, 'Book'),
        (2, 'Copy book'),
        (3, 'Diary'),
        (4, 'Magazine'),
        (5, 'Newspaper'),
        (6, 'Others'),
    ]
    book_type = models.IntegerField(choices=book_type_choice, default=-1)

    book_category_choice = [
        (-1, 'Select category'),
        (1, 'Fantasy'),
        (2, 'History'),
        (3, 'Mystery'),
        (4, 'Novel'),
        (5, 'Poetry'),
        (6, 'Thrillers'),
        (7, 'Others'),
    ]
    book_category = models.IntegerField(choices=book_category_choice, default=-1)
    objects = BookManager()

    def __str__(self):
        return self.name


class BookNote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(max_length=100)
    image = models.ImageField(upload_to='book_notes', blank=True, null=True)  # Додано поле для зображення
    book_note_created = models.DateField(verbose_name='Creation date', default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.book.name}"
