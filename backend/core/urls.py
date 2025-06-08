from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def home_view(request):
    return HttpResponse("Welcome to the homepage!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("API.urls")),
    path("", include("robot.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
