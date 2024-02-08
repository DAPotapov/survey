from django.db import DataError
from django.shortcuts import render, redirect
from .models import Question, Choice, Survey, UsersActivity
from .forms import SurveyForm


# Create your views here.
def index(request):
    # В задании указано требование "Без использования ORM" только перед требованиями к
    # результатам опросов. Следовательно, в остальных местах допускается использование ORM.
    surveys = Survey.objects.all()

    # Каждый запрос на главную страницу создаёт новую сессию
    request.session.create()    
    print(request.session.session_key)
    content = {
        'header': "Доступные опросы",
        'surveys': surveys
    }
    return render(request, 'main/index.html', content)


def treat_survey(request):
    if request.method == "POST":
        survey_id = request.POST.get("survey")
        survey = Survey.objects.get(pk=survey_id)
        request.session['survey'] = {
            'id': survey.id,
            'text': survey.text,
            'description': survey.description
        }
        err_code = '404'
        error = "Упс! Что-то пошло не так..."
        try:
            question = Question.objects.get(survey__id=survey_id, parent_question__isnull=True)
        except (Question.DoesNotExist, Question.MultipleObjectsReturned):
            return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
        else:        
            choices = Choice.objects.filter(question__id=question.id)
            if choices.exists():
                context = {
                    'header': "Опрос: " + survey_id,
                    'question': question,
                    'choices': choices
                    }
                return render(request, 'main/questions.html', context)
            else:
                return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
    else:
        return redirect("/")


def treat_answer(request):
    if request.method == "POST":
        err_code = '404'
        error = "Упс! Что-то пошло не так..."

        survey = request.session.get('survey', '')
        # Получаем информацию о вопросе и ответе на него из формы
        question_id, choosen_id = request.POST.get("choice").split('_')

        # Записываем полученную информацию в БД
        try:
            question = Question.objects.get(pk=question_id)
            choice = Choice.objects.get(pk=choosen_id)
            answer = UsersActivity(
                user_id=request.session.session_key,
                question=question,
                choice=choice
                )
            answer.save()
        except (
            Question.DoesNotExist,
            Question.MultipleObjectsReturned,
            Choice.DoesNotExist,
            Choice.MultipleObjectsReturned):
            return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
        except DataError:
            err_code = '500'
            error = 'Не удалось записать в базу данных. Попробуйте позже.'
            return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
        else:

            # Если ответ никуда не ведёт, значит опрос закончен и пора показывать результаты
            if not choice.next_question:
                try:
                    context = get_statistics(request.session.get('survey', '')['id'])
                except (AttributeError, ValueError):
                    return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
                else:
                    return render(request, 'main/results.html', context=context)
            
            # Готовим следующий вопрос и варианты ответа на
            try:
                question = choice.next_question
            except (Question.DoesNotExist, Question.MultipleObjectsReturned):
                return render(request, 'main/error.html', {'err_code': err_code, 'error': error})
            else:
                choices = question.choices.all()
                if choices.exists():
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
