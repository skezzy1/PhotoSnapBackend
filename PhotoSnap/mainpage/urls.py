from django.urls import path
from .views import BookView, BookNoteView, NoteStorageView

urlpatterns = [
    path('books/', BookView.book_list, name='book_list'),
    path('books/<int:book_id>/', BookView.book_detail, name='book_detail'),
    path('books/<int:book_id>/notes/', BookNoteView.book_notes, name='book_notes'),
    path('notestorage/', NoteStorageView.note_list, name = 'note_list'),
    path('notestorage/<int:note_id>', NoteStorageView.note_detail, name='note_detail'),
    path('notestorage/<init:note_id>/notes/', NoteStorageView.note_storage_notes, name='bookstorage_notes'),
]
