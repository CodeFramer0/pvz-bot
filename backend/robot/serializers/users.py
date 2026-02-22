from django.contrib.auth import get_user_model
from rest_framework import serializers

AppUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор пользователя.
    Используется для профиля (/me/) и CRUD операций.
    """

    class Meta:
        model = AppUser
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        )
        # Эти поля нельзя изменять вручную через API
        read_only_fields = ("id", "date_joined", "is_active")

    def validate_email(self, value):
        """Проверка уникальности email, если он меняется"""
        user = self.context['request'].user
        if AppUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value.lower()

    def validate_username(self, value):
        """Приведение username к нижнему регистру"""
        return value.lower()
