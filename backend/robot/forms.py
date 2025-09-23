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


class NewsletterForm(forms.Form):
    text = forms.CharField(
        label="Текст сообщения",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Введите текст..."}),
    )
    file = forms.FileField(label="Фото или файл", required=False)
