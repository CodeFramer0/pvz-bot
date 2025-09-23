import base64
import mimetypes

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from .forms import NewsletterForm
from .tasks import send_mass_telegram


@login_required(login_url="/admin/login/")
def newsletter_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Нет доступа.")
    if request.method == "POST":
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data["text"]
            file = request.FILES.get("file")

            file_data = None
            file_name = None
            is_image = False

            if file:
                content = file.read()
                file_data = base64.b64encode(content).decode("utf-8")
                file_name = file.name

                mime_type, _ = mimetypes.guess_type(file.name)
                is_image = mime_type and mime_type.startswith("image")

            send_mass_telegram.delay(
                text=text, file_data=file_data, file_name=file_name, is_image=is_image
            )

            return render(
                request,
                "newsletter_form.html",
                {"form": NewsletterForm(), "message": "Рассылка запущена!"},
            )

    else:
        form = NewsletterForm()
    return render(request, "newsletter_form.html", {"form": form})
