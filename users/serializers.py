from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import ConfirmationCode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserRegisterSerializer(UserBaseSerializer):

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError('User already exists!')

    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as error:
            raise ValidationError(error.messages)

        return password

class UserConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            confirmation = ConfirmationCode.objects.get(
                user_id=attrs['user_id'],
                code=attrs['code']
            )
        except ConfirmationCode.DoesNotExist:
            raise ValidationError('Неверный код подтверждения!')

        attrs['confirmation'] = confirmation
        return attrs