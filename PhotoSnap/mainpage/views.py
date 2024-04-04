from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _ 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .renders import BookRenderer

class BookView(APIView):
    renderer_classes = [BookRenderer]