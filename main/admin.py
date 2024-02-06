from django.contrib import admin
from .models import Question, Choice, UsersActivity, Survey


# Register your models here.
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UsersActivity)
