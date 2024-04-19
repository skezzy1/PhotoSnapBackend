from rest_framework import serializers
from .models import Book, BookNote
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _ 

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNote
        fields = '__all__'