from django.urls import path
from .views import BookView, BookNoteView, NoteStorageView, SearchView

urlpatterns = [
    #search url
    path('search/', SearchView.as_view(), name='search'),
    #books urls
    path('books/create', BookView.as_view(), name='book_create'),
    path('books/<int:book_id>/update', BookView.as_view(), name='book_update'),
    path('books/<int:book_id>/delete', BookView.as_view(), name='book_delete'),
    path('books/', BookView.as_view(), name='book_list'), 
    path('books/<int:book_id>', BookView.as_view(), name='book_detail'),
    path('books/<int:book_id>/sound', BookNoteView.as_view(), name='book_sound'),
    #books notes 
    path('books/<int:book_id>/notes', BookNoteView.as_view(), name='book_notes'),
    path('books/<int:book_id>/notes/create', BookNoteView.as_view(), name='create_book_note'),
    path('books/<int:book_id>/notes/<int:book_note_id>', BookNoteView.as_view(), name='book_note_detail'),
    path('books/<int:book_id>/notes/<int:book_note_id>/update', BookNoteView.as_view(), name='book_note_update'),
    path('books/<int:book_id>/notes/<int:book_note_id>/delete', BookNoteView.as_view(), name='book_note_delete'),
    path('books/<int:book_id>/notes/<int:book_note_id>/sound', BookNoteView.as_view(), name='book_note_sound'),
    #notes urls
    path('notestorage', NoteStorageView.as_view(), name='note_list'),
    path('notestorage/create', NoteStorageView.as_view(), name='note_create'),
    path('notestorage/<int:note_id>/update', NoteStorageView.as_view(), name='note_update'),
    path('notestorage/<int:note_id>/delete', NoteStorageView.as_view(), name='note_delete'),
    path('notestorage/<int:note_id>', NoteStorageView.as_view(), name='note_detail'), 
    path('notestorage/<int:note_id>/sound', NoteStorageView.as_view(), name='note_sound'), # Only one note from notestorage
    path('notestorage/sound', NoteStorageView.as_view(), name='notes_sound'), # All sound store 
]
