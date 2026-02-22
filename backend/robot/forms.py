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
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}), label="Текст")
    image = forms.ImageField(required=False, label="Картинка (опционально)")
    only_verified = forms.BooleanField(
        required=False, label="Только подтверждённые email"
    )
