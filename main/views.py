from django.shortcuts import render, redirect
from .models import Question, Choice, Survey
from .forms import SurveyForm


# Create your views here.
def index(request):
    # В задании указано требование "Без использования ORM" только перед требованиями к
    # результатам опросов. Следовательно, в остальных местах допускается использование ORM.
    surveys = Survey.objects.all()
    print(surveys)
    print(request)
    content = {
        'header': "Доступные опросы",
        'surveys': surveys
    }
    return render(request, 'main/index.html', content)


def treat_survey(request):
    print(request)
    if request.method == "POST":
        survey = request.POST.get("survey")
        err_code = '404'
        print(survey)  # тут должно быть id - ДА
        try:
            question = Question.objects.get(survey__id=survey, parent_question__isnull=True)
            print(question)
            choices = Choice.objects.filter(question__id=question.id)
            print(choices)
        except:
            error = "Упс! Что-то пошло не так..."
            return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
        else:        
            context = {
                'header': "Опрос: " + survey,
                'question': question,
                'choices': choices
                }
            return render(request, 'main/questions.html', context)


        # Теперь берем вопрос из БД и показываем варианты ответа, 
        # id заготавливаем для отдельного пользователя - храним в сессии - потом добавить
        # survey тоже лучше хранить в сессии, чтоб снизить нагрузку на БД
        # views должны быть разными, т.к. с формы survey получаю только id опроса
        # а с формы ответа на вопрос выбранный ответ - другая таблица!
        # городить длинный урл мне не надо, нужные данные я легко получу из choice.
            # TODO: в хедер помещаем название опроса
            # разбираем форму/реквест и 
            # в зависимости от содержимого выбираем из БД вопрос и варианты ответов.
            # полученные данные записываем в юзерактивити

            # также нужна будет проверка, что есть следующий вопрос, или нет
            # потом оптимизировать, т.к. эта процедура будет повторяться


    else:
        return redirect("/")


def treat_answer(request):
    if request.method == "POST":
        # Получаем id следующего вопроса из формы
        next_question_id = request.POST.get("choice")
        # TODO добавляем проверку на наличие вопроса и переход на страницу результатов
        # TODO записываем полученный результат! После введения сессии и id респондента
        err_code = '404'
        print("next_question_id: ", next_question_id)  # тут должно быть id 
        try:
            question = Question.objects.get(pk=next_question_id)
            choices = Choice.objects.filter(question__id=next_question_id)
        except:
            error = "Упс! Что-то пошло не так..."
            return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
        else:        
            survey = 'пока хардкод'
            context = {
                'header': survey,
                'question': question,
                'choices': choices
                }
            return render(request, 'main/questions.html', context)


    else:
        return redirect("/")
