from django.urls import path

from . import views

urlpatterns = [
    path("", views.CollectionsView.as_view(), name="collections"),
]
