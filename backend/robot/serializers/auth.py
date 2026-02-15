"""
robot/serializers/auth.py

Сериализаторы для аутентификации и управления пользователями
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

AppUser = get_user_model()


class EmailPasswordTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Получить токены по email и паролю"""

    username_field = AppUser.EMAIL_FIELD

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context.get("request")
        except KeyError:
            pass

        self.user = AppUser.objects.get(email=authenticate_kwargs["email"])
        if not self.user.check_password(authenticate_kwargs["password"]):
            raise serializers.ValidationError("Invalid credentials")

        return super().validate(attrs)


class UsernamePasswordTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Получить токены по username и паролю"""

    pass


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя (основной)"""

    class Meta:
        model = AppUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("id", "date_joined")


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = AppUser
        fields = (
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        )

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        if AppUser.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Пользователь с таким email уже существует"}
            )

        if AppUser.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Пользователь с таким username уже существует"}
            )

        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = AppUser.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации пользователя"""

    class Meta:
        model = AppUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("id", "date_joined", "last_login")
