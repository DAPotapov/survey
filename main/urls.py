from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("start_survey", views.start_survey, name="start_survey"),
]
