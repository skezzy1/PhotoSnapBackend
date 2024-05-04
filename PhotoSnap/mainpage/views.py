from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Book, BookNote, NoteStore
from .serializers import BookSerializer, BookNoteSerializer, NoteStorageSerializer

class BookView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id=None): 
        if book_id is not None: 
            book = get_object_or_404(Book, pk=book_id, user=request.user)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        else:
            books = Book.objects.filter(user=request.user)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
    def post(self, request):
        serializer = BookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id, user=request.user) 
        serializer = BookSerializer(book, data=request.data, context={'request': request}) 
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id, user=request.user)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class BookNoteView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, book_id=None, book_note_id=None): 
        if book_id is not None: 
            if book_note_id is not None:
                book_note = get_object_or_404(BookNote, pk=book_note_id, book_id=book_id)
                if book_note.user != request.user:
                    return Response({"error": "You don't have permission to access this content"}, status=status.HTTP_403_FORBIDDEN)
                serializer = BookNoteSerializer(book_note)
                return Response(serializer.data)
            else:
                book_notes = BookNote.objects.filter(user=request.user, book_id=book_id)
                serializer = BookNoteSerializer(book_notes, many=True)
                return Response(serializer.data)
        else:
            return Response({"error": "book_id parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookNoteSerializer(data=request.data, context={'request': request, 'book': book})
        if serializer.is_valid():
            serializer.save(user=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, book_id, book_note_id):
        book = get_object_or_404(Book, pk=book_id, user=request.user)
        note = get_object_or_404(BookNote, pk=book_note_id, book=book)
        serializer = NoteStorageSerializer(note, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, book_id, book_note_id):
        note = get_object_or_404(BookNote, pk=book_note_id, book__id=book_id, user=request.user)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class NoteStorageView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, note_id=None):
        notes = NoteStore.objects.filter(user=request.user)
        if note_id is not None:
            notes = get_object_or_404(notes, pk=note_id)
        serializer = NoteStorageSerializer(notes, many=note_id is None)
        return Response(serializer.data)
    def post(self, request):
        serializer = NoteStorageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, note_id):
        note = get_object_or_404(NoteStore, pk=note_id, user=request.user)
        serializer = NoteStorageSerializer(note, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = get_object_or_404(NoteStore, pk=note_id, user=request.user)
        note.delete()
        return Response({"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
