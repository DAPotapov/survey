from django.shortcuts import render, redirect
from .models import Question, Choice, Survey
from .forms import SurveyForm


# Create your views here.
def index(request):
    # В задании указано требование "Без использования ORM" только перед требованиями к
    # результатам опросов. Следовательно, в остальных местах допускается использование ORM.
    surveys = Survey.objects.all()
    content = {
        'header': "Доступные опросы",
        'choices': surveys
    }
    return render(request, 'main/index.html', content)


def treat_answer(request):
    error = ''
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()  # ????
            # TODO: в хедер помещаем название опроса
            # разбираем форму/реквест и 
            # в зависимости от содержимого выбираем из БД вопрос и варианты ответов.
            # полученные данные необходимо аккумулировать, 
            # чтобы записать в БД при окончании опроса
            # также нужна будет проверка, что есть следующий вопрос, или нет
            # потом оптимизировать, т.к. эта процедура будет повторяться
            # Выбор опроса можно расценивать как один из вопросов (1й)
            # 
            survey = "Здесь будет название опроса"
            question = "Здесь вопрос"
            choices = []
            context = {
                'header': survey,
                'question': question,
                'choices': choices
            }
            return render(request, 'main/index.html', context=context)
        else:
            error = 'Форма заполнена неверно'
    context = {
        'header': error,
        'choices': ''
    }
    return render(request, 'main/index.html', context=context)
