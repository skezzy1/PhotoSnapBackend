from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .models import RegisterUser
from .serializers import RegisterUserSerializer

@api_view(['GET', 'POST'])
def register_user_list(request):
    if request.method == 'GET':
        users = RegisterUser.objects.all()
        serializer = RegisterUserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) #and redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    # Код для обробки реєстрації користувача
    return Response({"message": "User registration successful"})
