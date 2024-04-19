from django.db import models
from accounts.models import BaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField

class Book(models.Model):   
    book_id = models.AutoField(primary_key=True)
    book_image = CloudinaryField('image')
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)  
    author = models.CharField(max_length=100, blank=True)  
    book_time_created = models.DateTimeField(default=timezone.now)

    BOOK_TYPE_CHOICES = [
        (1, 'Book'),
        (2, 'Copy book'),
        (3, 'Diary'),
        (4, 'Magazine'),
        (5, 'Newspaper'),
        (6, 'Others'),
    ]
    book_type = models.IntegerField(choices=BOOK_TYPE_CHOICES, default=1)

    BOOK_CATEGORY_CHOICES = [
        (1, 'Fantasy'),
        (2, 'History'),
        (3, 'Mystery'),
        (4, 'Novel'),
        (5, 'Poetry'),
        (6, 'Thrillers'),
        (7, 'Others'),
    ]
    book_category = models.IntegerField(choices=BOOK_CATEGORY_CHOICES, default=1)

    def __str__(self):
        return self.book_name


class BookNote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=100) 
    book_note_created = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Note for {self.book.book_name}"

class NoteStore(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    note_id = models.AutoField(primary_key=True)
    note = models.TextField(max_length=100)
    note_created = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Note for {self.user.username}"