from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("survey", views.treat_answer, name="treat_answer"),
]
