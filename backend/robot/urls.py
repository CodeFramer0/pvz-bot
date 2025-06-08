from django.urls import path

from .views import newsletter_view

urlpatterns = [
    path('newsletter/', newsletter_view, name='newsletter')
]
