# robot/management/commands/fill_appusers.py
from django.core.management.base import BaseCommand
from robot.models import TelegramUser, AppUser

class Command(BaseCommand):
    help = "Создает AppUser для всех TelegramUser, у которых его нет"

    def handle(self, *args, **kwargs):
        tg_users = TelegramUser.objects.filter(app_user__isnull=True)
        for tg in tg_users:
            user = AppUser.objects.create(
                username=f"tg_{tg.user_id}",
                is_active=True,
            )
            tg.app_user = user
            tg.save()
            self.stdout.write(self.style.SUCCESS(f"Создан AppUser {user.username} для TG {tg.nick_name}"))