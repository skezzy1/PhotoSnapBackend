from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Book, BookNote, NoteStore

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    def validate(self, attrs):
        book_name = attrs.get('book_name')
        if book_name and Book.objects.filter(book_name=book_name).exists():
            raise serializers.ValidationError("A book with this name already exists.")
        return attrs
    def update(self, instance, validated_data):
        instance.book_name = validated_data.get('book_name', instance.book_name)
        instance.user = validated_data.get('user', instance.user)
        instance.author = validated_data.get('author', instance.author)
        instance.book_image = validated_data.get('book_image', instance.book_image)
        instance.book_time_created = validated_data.get('book_time_created', instance.book_time_created)
        instance.book_type = validated_data.get('book_type', instance.book_type)
        instance.book_category = validated_data.get('book_category', instance.book_category)
        instance.save()
        return instance
    
class BookNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNote
        fields = '__all__'
    def create(self, validated_data):
        book_id = self.context['book_id'] 
        book = get_object_or_404(Book, pk=book_id)
        note = BookNote.objects.create(book=book, **validated_data)
        return note
class NoteStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteStore
        fields = '__all__'
        