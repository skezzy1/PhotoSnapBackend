from django.urls import path
from .views import BookView, BookNoteView, NoteStorageView

urlpatterns = [
    #books urls
    path('books/create', BookView.as_view(), name='book_create'),
    path('books/<int:book_id>/update', BookView.as_view(), name='book_update'),
    path('books/<int:book_id>/delete', BookView.as_view(), name='book_delete'),
    path('books/', BookView.as_view(), name='book_list'), 
    path('books/<int:book_id>', BookView.as_view(), name='book_detail'),
    #books notes 
    path('books/<int:book_id>/notes/create', BookView.as_view(), name='book_note_create'),
    path('books/<int:book_id>/notes/<int:note_id>/update', BookView.as_view(), name='book_note_update'),
    path('books/<int:book_id>/notes/<int:note_id>/delete', BookView.as_view(), name='book_note_delete'),
    path('books/<int:book_id>/notes/<int:note_id>/sound', BookView.as_view(), name='book_note_sound'),
    path('books/<int:book_id>/notes', BookNoteView.as_view(), name='book_notes'),
    path('books/<int:book_id>/sound', BookNoteView.as_view(), name='book_sound'),
    #notes urls
    path('notestorage/', NoteStorageView.as_view(), name='note_list'),
    path('notestorage/create/', NoteStorageView.as_view(), name='note_create'),
    path('notestorage/<int:note_id>/update', NoteStorageView.as_view(), name='note_update'),
    path('notestorage/<int:note_id>/delete', NoteStorageView.as_view(), name='note_delete'),
    path('notestorage/<int:note_id>', NoteStorageView.as_view(), name='note_detail'),  
]
