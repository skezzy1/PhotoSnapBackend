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
        book = get_object_or_404(Book, pk=book_id, user=request.user)  # Ensure user is also checked here
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

    def get(self, request, book_note_id=None): 
        if book_note_id is not None: 
            book_note = get_object_or_404(BookNote, pk=book_note_id)
            if book_note.book.user != request.user:
                return Response({"error": "You don't have permission to access this content"}, status=status.HTTP_403_FORBIDDEN)
            serializer = BookNoteSerializer(book_note)
            return Response(serializer.data)
        else:
            book_notes = BookNote.objects.filter(book__user=request.user)
            serializer = BookNoteSerializer(book_notes, many=True)
            return Response(serializer.data)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id, user=request.user)
        serializer = BookNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, book_note_id):
        note = get_object_or_404(BookNote, pk=book_note_id)
        if note.book.user != request.user:
            return Response({"error": "You don't have permission to access this content"}, status=status.HTTP_403_FORBIDDEN)
        serializer = BookNoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_note_id):
        note = get_object_or_404(BookNote, pk=book_note_id)
        if note.book.user != request.user:
            return Response({"error": "You don't have permission to access this content"}, status=status.HTTP_403_FORBIDDEN)
        note.delete()
        return Response({"message": "BookNote deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class NoteStorageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, note_id=None): 
        if note_id is not None: 
            note = get_object_or_404(NoteStore, pk=note_id)
            serializer = NoteStorageSerializer(note)
            return Response(serializer.data)
        else:
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
