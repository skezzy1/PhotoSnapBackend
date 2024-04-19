from django.contrib import admin
from .models import Book, BookNote, NoteStore

admin.site.register(Book)
admin.site.register(BookNote)
admin.site.register(NoteStore)