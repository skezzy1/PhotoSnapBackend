from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .serializers import BaseUserSerializer
from .models import BaseUser  

@api_view(['GET', 'POST'])
def register_user_list(request):
    if request.method == 'GET':
        users = BaseUser.objects.all()
        serializer = BaseUserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BaseUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = BaseUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('home')  # Redirect to your home page
    else:
        serializer = BaseUserSerializer()
    return Response(serializer.data)
