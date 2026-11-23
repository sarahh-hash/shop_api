import secrets

from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema

from users.serializers import (
    RegisterValidateSerializer,
    AuthValidateSerializer,
    ConfirmationSerializer
)

from users.models import ConfirmationCode, CustomUser


@swagger_auto_schema(
    method='post',
    request_body=RegisterValidateSerializer
)
@api_view(['POST'])
def registration_api_view(request):

    serializer = RegisterValidateSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')

    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        is_active=False
    )

    code = str(secrets.randbelow(900000) + 100000)

    ConfirmationCode.objects.create(
        user=user,
        code=code
    )

    return Response(
        data={'user_id': user.id},
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='post',
    request_body=AuthValidateSerializer
)
@api_view(['POST'])
def authorization_api_view(request):

    serializer = AuthValidateSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    user = authenticate(
        request,
        email=serializer.validated_data.get('email'),
        password=serializer.validated_data.get('password')
    )

    if user:

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            data={'key': token.key},
            status=status.HTTP_200_OK
        )

    return Response(
        data={'message': 'Неверный логин или пароль!'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@swagger_auto_schema(
    method='post',
    request_body=ConfirmationSerializer
)
@api_view(['POST'])
def confirmation_api_view(request):

    serializer = ConfirmationSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    user_id = serializer.validated_data.get('user_id')

    user = CustomUser.objects.get(id=user_id)

    user.is_active = True
    user.save()

    ConfirmationCode.objects.get(user=user).delete()

    return Response(
        data={'message': 'Пользователь успешно подтверждён!'},
        status=status.HTTP_200_OK
    )