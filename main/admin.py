from django.contrib import admin
from .models import Questions, Choices, Users, UsersActivity, Surveys


# Register your models here.
admin.site.register(Surveys)