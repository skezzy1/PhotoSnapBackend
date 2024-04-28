from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Book, BookNote, NoteStore
from .serializers import BookSerializer, BookNoteSerializer, NoteStorageSerializer

class BookView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, book_id=None): 
        if book_id is not None: 
            return self.book_detail(request, book_id) 
        else:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def edit(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def book_detail(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

class BookNoteView(APIView):
    permission_classes = [IsAuthenticated]
    def book_notes(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        notes = BookNote.objects.filter(book=book)
        serializer = BookNoteSerializer(notes, many=True)
        return Response(serializer.data)

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        notes = BookNote.objects.filter(book=book)
        serializer = BookNoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookNoteSerializer(data=request.data, context={'book': book})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUES)

    def put(self, request, book_id, book_note_id):
        note = get_object_or_404(BookNote, pk=book_note_id)
        serializer = BookNoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_note_id):
        note = get_object_or_404(BookNote, pk=book_note_id)
        note.delete()
        return Response({"message": "BookNote deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class NoteStorageView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, note_id=None): 
        if note_id is not None: 
            return self.note_detail(request, note_id) 
        else:
            notes = NoteStore.objects.all()
            serializer = NoteStorageSerializer(notes, many=True)
            return Response(serializer.data)

    def note_list(self, request):
        notes = NoteStore.objects.all()
        serializer = NoteStorageSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteStorageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, note_id):
        note = get_object_or_404(NoteStore, pk=note_id)
        serializer = NoteStorageSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, note_id):
        note = get_object_or_404(NoteStore, pk=note_id)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    def note_detail(self, request, note_id):
        note = get_object_or_404(NoteStore, pk=note_id)
        serializer = NoteStorageSerializer(note)
        return Response(serializer.data)