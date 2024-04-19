from rest_framework import serializers
from .models import Book, BookNote, NoteStore

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNote
        fields = '__all__'
class NoteStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteStore
        fields = '__all__'