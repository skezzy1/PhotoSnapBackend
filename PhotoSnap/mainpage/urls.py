from django.urls import path
from .views import BookView, BookNoteView

urlpatterns = [
    path('books/', BookView.book_list, name='book_list'),
    path('books/<int:book_id>/', BookView.book_detail, name='book_detail'),
    path('books/<int:book_id>/notes/', BookNoteView.book_notes, name='book_notes'),
]
