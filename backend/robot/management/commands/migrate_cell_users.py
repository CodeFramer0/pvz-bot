from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.crypto import get_random_string
from robot.models import Order, TelegramUser

AppUser = get_user_model()


class Command(BaseCommand):
    help = "Создать AppUser для всех TelegramUser и перепривязать заказы"

    def handle(self, *args, **kwargs):
        created_count = 0
        reassigned_count = 0

        with transaction.atomic():
            for tg in TelegramUser.objects.all():
                # создаём AppUser с id = TelegramUser.id
                user, created = AppUser.objects.get_or_create(
                    id=tg.id,
                    defaults={
                        "username": f"{tg.nick_name or 'user'}_{get_random_string(6)}",
                        "is_active": True,
                    },
                )
                if created:
                    created_count += 1

                # привязываем TelegramUser
                tg.app_user = user
                tg.save()

                # перепривязываем заказы
                orders = Order.objects.filter(customer_id=tg.id)
                orders.update(customer_id=user.id)
                reassigned_count += orders.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Создано AppUser-ов: {created_count}, заказов перепривязано: {reassigned_count}"
            )
        )
