from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Пример маршрута
    path("", views.index, name="index"),
]
