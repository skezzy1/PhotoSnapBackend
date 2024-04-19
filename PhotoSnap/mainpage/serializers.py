from rest_framework import serializers
from .models import Book, BookNote, BookStore
from django.utils.translation import gettext_lazy as _ 

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
        model = BookStore
        fields = '__all__'