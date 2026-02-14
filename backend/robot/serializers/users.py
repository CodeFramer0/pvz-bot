"""
robot/serializers/users.py

Сериализаторы для пользователей приложения
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

AppUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Основной сериализатор пользователя"""
    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        
        if AppUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email уже существует"})
        
        if AppUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Пользователь с таким username уже существует"})
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = AppUser.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации пользователя"""
    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 
                  'is_staff', 'date_joined', 'last_login')
        read_only_fields = ('id', 'date_joined', 'last_login')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления пользователя"""
    class Meta:
        model = AppUser
        fields = ('username', 'email', 'first_name', 'last_name')

    def validate_email(self, value):
        # Проверяем, не используется ли этот email другим пользователем
        user = self.instance
        if AppUser.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def validate_username(self, value):
        # Проверяем, не используется ли этот username другим пользователем
        user = self.instance
        if AppUser.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("Пользователь с таким username уже существует")
        return value
