# robot/management/commands/fix_orders_fk.py
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Создает AppUser для всех customer_id из orders.json, чтобы фикстуры Orders загрузились"

    def add_arguments(self, parser):
        parser.add_argument(
            '--orders-file',
            type=str,
            default='orders.json',
            help='Путь к orders.json',
        )

    def handle(self, *args, **options):
        orders_file = Path(options['orders_file'])
        if not orders_file.exists():
            self.stderr.write(self.style.ERROR(f"Файл {orders_file} не найден"))
            return

        with open(orders_file) as f:
            orders = json.load(f)

        # собираем все уникальные customer_id
        customer_ids = set(order['fields']['customer'] for order in orders)
        self.stdout.write(self.style.SUCCESS(f"Найдено {len(customer_ids)} уникальных customer_id"))

        created = 0
        for cid in customer_ids:
            if not User.objects.filter(id=cid).exists():
                User.objects.create(
                    id=cid,  # важно: id совпадает с тем, что в orders.json
                    username=f"user_{cid}",
                    is_active=True
                )
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Создан AppUser с id={cid}"))

        self.stdout.write(self.style.SUCCESS(f"Готово! Создано {created} новых AppUser."))