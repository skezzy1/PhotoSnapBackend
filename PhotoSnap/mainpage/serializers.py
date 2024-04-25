from rest_framework import serializers
from .models import Book, BookNote, NoteStore

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    def validate(self, attrs):
        if attrs['book_name'] == attrs['book_name']:
            raise serializers.ValidationError("Book name is already taken, can't be same")
        return super().validate(attrs)
class BookNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNote
        fields = '__all__'
class NoteStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteStore
        fields = '__all__'