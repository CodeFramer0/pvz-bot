from django.core.management.base import BaseCommand
from robot.models import Marketplace, Order, PickupPoint


class Command(BaseCommand):
    help = "Объединяет ПВЗ по адресу в одну запись с marketplaces"

    def handle(self, *args, **options):
        marketplace_map = {
            "ozon": "Озон",
            "wb": "ВБ",
            "yandex": "Яндекс Маркет",
            "cdek": "СДЭК",
            "mail": "Почта России +150₽",
        }

        marketplaces = {}
        for code, name in marketplace_map.items():
            obj, _ = Marketplace.objects.get_or_create(
                code=code, defaults={"name": name}
            )
            marketplaces[code] = obj

        old_points = list(PickupPoint.objects.all())

        by_address = {}
        for pp in old_points:
            by_address.setdefault(pp.address, []).append(pp)

        self.stdout.write(f"Найдено старых ПВЗ: {len(old_points)}")
        self.stdout.write(f"Уникальных адресов: {len(by_address)}")

        updated_orders = 0
        removed_pp = 0

        for address, points in by_address.items():
            main_pp = points[0]

            for old in points:
                mp_code = getattr(old, "marketplace", None)
                if mp_code:
                    mp = marketplaces.get(mp_code)
                    if mp:
                        main_pp.marketplaces.add(mp)

            # перенос заказов с дубликатов
            for dup in points[1:]:
                updated = Order.objects.filter(pickup_point=dup).update(
                    pickup_point=main_pp
                )
                updated_orders += updated
                dup.delete()
                removed_pp += 1

        self.stdout.write(f"Обновлено заказов: {updated_orders}")
        self.stdout.write(f"Удалено дубликатов ПВЗ: {removed_pp}")
        self.stdout.write(self.style.SUCCESS("Готово. ПВЗ успешно объединены."))
