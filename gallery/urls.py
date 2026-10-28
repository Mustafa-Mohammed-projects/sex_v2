from django.urls import path
from . import views

app_name = "gallery"
urlpatterns = [
    path("", views.home, name="home"),
    path("m/<int:pk>/", views.detail, name="detail"),
]
