from rest_framework import serializers
from .models import Book
from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _ 
from rest_framework.views import APIView

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_name', 'author', 'book_type', 'book_category']
        