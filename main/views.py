from django.shortcuts import render, redirect
from .models import Question, Choice, Survey
from .forms import SurveyForm


# Create your views here.
def index(request):
    surveys = Survey.objects.all()
    content = {
        'header': "Доступные опросы",
        'surveys': surveys
    }
    return render(request, 'main/index.html', content)


def start_survey(request):
    error = ''
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            error = 'Форма заполнена неверно'
    context = {
        'header': error,
        'surveys': ''
    }
    return render(request, 'main/index.html', context=context)
