from django import forms

from .models import PickupPoint, TelegramUser


class PickPointForm(forms.ModelForm):
    class Meta:
        model = PickupPoint
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PickPointForm, self).__init__(*args, **kwargs)
        self.fields["admin_telegram_user"].queryset = TelegramUser.objects.filter(
            is_administrator=True
        )
