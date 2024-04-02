from django.db import models
from accounts.models import BaseUser

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length = 100, blank=True)
    BOOK = 'Book'
    COPY_BOOK='Copy book'
    DIARY='Diary'
    MAGAZINE = 'Magazine'
    NEWSPAPER= 'Newspaper'
    OTHERS = "Others"
    book_type_choice= [(BOOK, 'Book'),
                       (COPY_BOOK, 'Copy book'),
                       (DIARY,'Diary'),
                       (MAGAZINE,'Magazine'),
                       (NEWSPAPER, 'Newspaper'),
                       (OTHERS, 'Others'),
                       ]
    FANTASY = 'Fantasy'
    HISTORY = 'History' 
    MYSTERY = 'Mystery'
    NOVEL = 'Novel'
    POETRY = 'Poetry'
    THRILLERS = 'Thillers'
    OTHERS = "Others"
    book_category_choice = [(FANTASY, 'Fantasy'),
                            (HISTORY, 'History'),
                            (MYSTERY,"Mystery"),
                            (NOVEL, 'Novel'),
                            (POETRY, 'Poetry'),
                            (THRILLERS, 'Thrillers'),
                            (OTHERS, 'Others'),
                            ]
    USERNAME_FIELD = 'book_name'
    REQUIRED_FIELDS = ['book_type_choice', 'book_category_choice']
    
    def __str__(self): 
         return self.book_name
                             
    