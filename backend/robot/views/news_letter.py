from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

from ..serializers import NewsletterSerializer
from ..tasks import send_mass_telegram

class NewsletterAPIView(generics.GenericAPIView):
    """
    Рассылка сообщений пользователям через Telegram.
    Доступно только администраторам.
    """
    permission_classes = [IsAdminUser]
    serializer_class = NewsletterSerializer
    # Важно: без этих парсеров Swagger не покажет кнопку выбора файла
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        summary="Запустить массовую рассылку",
        description="Принимает текст и опциональное изображение. Ставит задачу в Celery.",
        tags=["Admin Operations"],
        responses={200: {"detail": "Рассылка запущена"}}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data["text"]
        image = serializer.validated_data.get("image")
        only_verified = serializer.validated_data.get("only_verified", False)

        image_path = None
        if image:
            # Сохраняем файл, чтобы передать путь в Celery (сам файл передать в таску нельзя)
            image_path = default_storage.save(f"newsletter/{image.name}", image)

        # Запуск фоновой задачи
        send_mass_telegram.delay(text, image_path, only_verified)
        
        return Response(
            {"detail": "Рассылка успешно добавлена в очередь"}, 
            status=status.HTTP_200_OK
        )
