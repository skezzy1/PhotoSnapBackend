from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Book, BookNote, NoteStore
from .serializers import BookSerializer, BookNoteSerializer, NoteStorageSerializer
from .renders import BookRenderer

class BookView(APIView):
    renderer_classes = [BookRenderer]
    permission_classes = [IsAuthenticated]
    def book_list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    def book_detail(self, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book, may=True)
        return Response(serializer.data)
class BookNoteView(APIView):
    renderer_classes = [BookRenderer]
    permission_classes = [IsAuthenticated]
    def book_notes(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        notes = BookNote.objects.filter(book=book)
        serializer = BookNoteSerializer(notes, many=True)
        return Response(serializer.data)
class NoteStorageView(APIView):
    renderer_classes = [BookRenderer]
    permission_classes = [IsAuthenticated]
    def note_list(self):
        notes = NoteStore.objects.all()
        serializer = NoteStorageSerializer(notes, many=True)
        return Response(serializer.data)
    def note_detail(self, note_id):
        notes = get_object_or_404(notes, pk=note_id)
        serializer = NoteStorageSerializer(notes, many=True)
        return Response(serializer.data)