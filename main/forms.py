from .models import Choice, Question, Survey
from django.forms import ModelForm


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ["text", "description"]