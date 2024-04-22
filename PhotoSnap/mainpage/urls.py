from django.urls import path
from .views import BookView, BookNoteView, NoteStorageView

urlpatterns = [
    path('books/', BookView.as_view(), name='book_list'), 
    path('books/<int:book_id>/', BookView.as_view(), name='book_detail'),
    path('books/<int:book_id>/notes/', BookNoteView.as_view(), name='book_notes'),
    path('notestorage/', NoteStorageView.as_view(), name='note_list'),
    path('notestorage/<int:note_id>/', NoteStorageView.as_view(), name='note_detail'),  
]
