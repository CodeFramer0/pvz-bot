# Generated by Django 5.1.2 on 2024-11-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("robot", "0006_alter_pickuppoint_marketplace"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="ammount",
            field=models.CharField(
                default="0", max_length=128, verbose_name="Сумма заказа"
            ),
        ),
    ]
