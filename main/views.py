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
        error = "Упс! Что-то пошло не так..."
        print(survey)  # тут должно быть id - ДА
        try:
            question = Question.objects.get(survey__id=survey, parent_question__isnull=True)
            print(question)
        except (Question.DoesNotExist, Question.MultipleObjectsReturned):
            return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
        else:        
            choices = Choice.objects.filter(question__id=question.id)
            if choices.exists():
                print(choices)
                context = {
                    'header': "Опрос: " + survey,
                    'question': question,
                    'choices': choices
                    }
                return render(request, 'main/questions.html', context)
            else:
                return render(request, 'main/error.html', {'err_code': err_code, 'error': error})



        # id заготавливаем для отдельного пользователя - храним в сессии - потом добавить
        # survey тоже лучше хранить в сессии, чтоб снизить нагрузку на БД
        # views должны быть разными, т.к. с формы survey получаю только id опроса
 
            # TODO: в хедер помещаем название опроса
            # разбираем форму/реквест и 
            # в зависимости от содержимого выбираем из БД вопрос и варианты ответов.
            # полученные данные записываем в юзерактивити

            # потом оптимизировать, т.к. эта процедура будет повторяться


    else:
        return redirect("/")


def treat_answer(request):
    if request.method == "POST":
        question_id, choosen_id = request.POST.get("choice").split('_') # Его и запишем в БД
        print("choice from form:", choosen_id, type(choosen_id))
        next_question = Choice.objects.get(pk=choosen_id).next_question
        # TODO записываем полученный результат! После введения сессии и id респондента

        # Если ответ никуда не ведёт, значит опрос закончен и пора показывать результаты
        if not next_question:
            context = get_statistics(1)
            return render(request, 'main/results.html', context=context)
        
        err_code = '404'
        error = "Упс! Что-то пошло не так..."
        print("next_question_id: ", next_question, type(next_question), next_question.id)  # тут должно быть id 
        try:
            question = Question.objects.get(pk=next_question.id)
            print("question_id: ", question, type(question), question.id)
        except (Question.DoesNotExist, Question.MultipleObjectsReturned):
            return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
        else:
            print("Они одинаковые?", question is next_question)
            choices = Choice.objects.filter(question__id=next_question.id)
            if choices.exists():
                survey = 'пока хардкод'
                context = {
                    'header': survey,
                    'question': question,
                    'choices': choices
                    }
                return render(request, 'main/questions.html', context)
            else:
                return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
    else:
        return redirect("/")


def get_statistics(survey_id):
    context = {}
    return context
