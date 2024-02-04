from django.shortcuts import render
from .models import Question, Choice, Survey


# Create your views here.
def index(request):
    surveys = Survey.objects.all()
    content = {
        'header': "Доступные опросы",
        'surveys': surveys
    }
    return render(request, 'main/index.html', content)
