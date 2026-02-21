from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from ..forms import NewsletterForm
from ..tasks import send_mass_telegram

@staff_member_required
def newsletter_view(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data["text"]
            image = form.cleaned_data.get("image")
            only_verified = form.cleaned_data.get("only_verified")

            image_path = None
            if image:
                from django.core.files.storage import default_storage
                image_path = default_storage.save(f"newsletter/{image.name}", image)

            send_mass_telegram.delay(text, image_path, only_verified)
            return render(request, "newsletter_form.html", {"form": form, "message": "Рассылка запущена"})
    else:
        form = NewsletterForm()

    return render(request, "newsletter_form.html", {"form": form})