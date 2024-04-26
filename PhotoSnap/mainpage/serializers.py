from rest_framework import serializers
from .models import Book, BookNote, NoteStore

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    def validate(self, attrs):
        book_name = attrs.get('book_name', None)
        if book_name:
            if Book.objects.filter(book_name=book_name).exists():
                raise serializers.ValidationError("A book with this name already exists.")
            return attrs
class BookNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNote
        fields = '__all__'
class NoteStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteStore
        fields = '__all__'