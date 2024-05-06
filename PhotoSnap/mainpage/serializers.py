from rest_framework import serializers
from .models import Book, BookNote, NoteStore

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }
    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        book_name = attrs.get('book_name')
        if Book.objects.filter(book_name=book_name, user=user).exists():
            raise serializers.ValidationError("A book with this name already exists for this user.")
        return attrs
    def update(self, instance, validated_data):
        instance.book_name = validated_data.get('book_name', instance.book_name)
        instance.author = validated_data.get('author', instance.author)
        instance.book_image = validated_data.get('book_image', instance.book_image)
        instance.book_type = validated_data.get('book_type', instance.book_type)
        instance.book_category = validated_data.get('book_category', instance.book_category)
        instance.save()
        return instance
    
class BookNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNote
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'book':{'required': False}
        }
    def create(self, validated_data):
        note = BookNote.objects.create(**validated_data)
        return note

    def update(self, instance, validated_data):
        instance.book_note_name = validated_data.get('book_note_name', instance.book_note_name)
        instance.book_note_content = validated_data.get('book_note_content', instance.book_note_content) 
        instance.save()
        return instance
class NoteStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteStore
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }