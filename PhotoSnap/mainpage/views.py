from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Book, BookNote, NoteStore
from .serializers import BookSerializer, BookNoteSerializer, NoteStorageSerializer

class BookView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): 
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def book_detail(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def book_notes(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        notes = BookNote.objects.filter(book=book)
        serializer = BookNoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookNoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NoteStorageView(APIView):
    permission_classes = [IsAuthenticated]

    def note_list(self, request):
        notes = NoteStore.objects.all()
        serializer = NoteStorageSerializer(notes, many=True)
        return Response(serializer.data)

    def note_detail(self, request, note_id):
        note = get_object_or_404(NoteStore, pk=note_id)
        serializer = NoteStorageSerializer(note)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteStorageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
