from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserRegisterSerializer,
    UserAuthSerializer,
    UserConfirmSerializer
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    ConfirmationCode.objects.create(user=user)

    return Response(
        data={'user_id': user.id},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})

    return Response(
        data={'message': 'Неверный логин или пароль!'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
def confirmation_api_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    confirmation = serializer.validated_data.get('confirmation')
    user = confirmation.user

    user.is_active = True
    user.save()

    confirmation.delete()

    return Response(
        data={'message': 'Пользователь успешно подтверждён!'},
        status=status.HTTP_200_OK
    )