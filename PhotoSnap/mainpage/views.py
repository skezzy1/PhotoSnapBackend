from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Book, BookNote, NoteStore
from .serializers import BookSerializer, BookNoteSerializer, NoteStorageSerializer
from rest_framework import generics
from django.db.models import Q

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
        serializer = BookNoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, book=book) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, **kwargs):
        book_note_id = kwargs.get('book_note_id')
        book_id = kwargs.get('book_id')
        book_note = get_object_or_404(BookNote, pk=book_note_id, user=request.user)
        book = get_object_or_404(Book, pk=book_id, user=request.user)
        note_serializer = BookNoteSerializer(book_note, data=request.data, context={'request': request}, partial=True)
        if note_serializer.is_valid():
            note_serializer.save(user=request.user)
            return Response(note_serializer.data, status=status.HTTP_201_CREATED)
        return Response(note_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, **kwargs):
        book_note_id = kwargs.get('book_note_id')
        book_note = get_object_or_404(BookNote, pk=book_note_id, user=request.user)
        book_note.delete()
        return Response({"message": "Book note deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

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

class SearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields_book = ['author', 'book_name', 'book_type', 'book_category']
    search_fields_note = ['book_note_name', 'book_note_content']
    search_fields_storage = ['note_name', 'note_content']

    def get_queryset(self):
        user_identifier = self.request.user.user_id
        query = self.request.query_params.get('search', None)
        queryset_book = Book.objects.none()
        queryset_note = BookNote.objects.none()
        queryset_storage = NoteStore.objects.none()

        if query:
            for field in self.search_fields_book:
                queryset_book |= Book.objects.filter(user=user_identifier, **{f"{field}__icontains": query})
            for field in self.search_fields_note:
                queryset_note |= BookNote.objects.filter(user=user_identifier, **{f"{field}__icontains": query})
            for field in self.search_fields_storage:
                queryset_storage |= NoteStore.objects.filter(user=user_identifier, **{f"{field}__icontains": query})

        return queryset_book, queryset_note, queryset_storage

    def list(self, request, *args, **kwargs):
        queryset_book, queryset_note, queryset_storage = self.get_queryset()
        serializer_book = BookSerializer(queryset_book, many=True)
        serializer_note = BookNoteSerializer(queryset_note, many=True)
        serializer_storage = NoteStorageSerializer(queryset_storage, many=True)
        return Response(serializer_book.data + serializer_note.data + serializer_storage.data)
