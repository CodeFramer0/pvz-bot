from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from robot.models import PickupPoint, TelegramUser


class PickPointForm(forms.ModelForm):
    class Meta:
        model = PickupPoint
        fields = "__all__"
        widgets = {
            "marketplaces": FilteredSelectMultiple("Маркетплейсы", is_stacked=False),
        }


class NewsletterForm(forms.Form):
    text = forms.CharField(
        label="Текст сообщения",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Введите текст..."}),
    )
    file = forms.FileField(label="Фото или файл", required=False)
