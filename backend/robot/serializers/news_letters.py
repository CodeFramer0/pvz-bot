from rest_framework import serializers

class NewsletterSerializer(serializers.Serializer):
    """
    Сериализатор для создания массовой рассылки через Telegram.
    """
    text = serializers.CharField(
        help_text="Текст сообщения для рассылки",
        style={'base_template': 'textarea.html'} # Подсказка для рендеринга в UI
    )
    image = serializers.ImageField(
        required=False, 
        allow_null=True,
        help_text="Опциональное изображение для вложения"
    )
    only_verified = serializers.BooleanField(
        default=False,
        help_text="Отправлять только верифицированным пользователям"
    )

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст рассылки не может быть пустым.")
        return value
