from django.db import DataError, connections
from django.shortcuts import render, redirect

from .models import Question, Choice, Survey, UsersActivity


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
                    context = get_results(request.session.get('survey', '')['id'])
                    context['survey'] = survey
                except (AttributeError, ValueError, IndexError, TypeError):
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


def get_results(survey_id):
    db_name = 'default'
    conn = connections[db_name]
    context = {}
    with conn.cursor() as cursor:
        
        # Количество участников опроса
        query = "SELECT COUNT(DISTINCT user_id) FROM main_usersactivity WHERE question_id IN (SELECT id FROM main_question WHERE survey_id=%s)"
        cursor.execute(query, [survey_id])
        respondent_count = cursor.fetchone()[0]

        # Количество ответивших на каждый вопрос и их доля от общего числа респондентов опроса
        query = """
            WITH ranked_users_activity AS (
            SELECT
                question_id,
                COUNT(*) AS record_count,
                DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS position
            FROM
                main_usersactivity
            WHERE question_id in (
                SELECT id FROM main_question WHERE survey_id = %s)
            GROUP BY
                question_id
            )
            SELECT
                question_id,
                main_question.text,
                record_count,
                position
            FROM
                ranked_users_activity
            JOIN
                main_question ON question_id = main_question.id
            """
        cursor.execute(query, [survey_id])
        questions = cursor.fetchall()

        # Получим статистику по сделанным выборам
        query = """
            WITH choosen_stats AS
                (SELECT 
                    choice_id, COUNT(*) as choice_count 
                FROM 
                    main_usersactivity 
                WHERE question_id IN (
                    SELECT id 
                    FROM 
                        main_question 
                    WHERE 
                        survey_id=%s)  
                    GROUP BY 
                        choice_id)
            SELECT 
                main_choice.text,
                question_id,
                choice_count
            FROM
                choosen_stats	
            JOIN 
                main_choice ON main_choice.id=choice_id;
        """
        cursor.execute(query, [survey_id])
        choices = cursor.fetchall()
            
        # Объединим полученные данные преобразовав в словарь
        c_keys = ['text', 'question_id', 'choice_count']
        new_questions = []
        q_keys = ['id', 'text', 'record_count', 'position']
        for q in questions:
            question = dict(zip(q_keys, q))
            q_choices = []
            for c in choices:
                choice_dict = dict(zip(c_keys, c))
                if choice_dict['question_id'] == question['id']:
                    choice_dict['rate'] = choice_dict['choice_count'] / question['record_count'] * 100  # процент
                    q_choices.append(choice_dict)
            question['choices'] = q_choices
            question['rate'] = question['record_count'] / respondent_count * 100  # процент
            print(question)
            new_questions.append(question)

        # Соберём словарь для передачи в шаблон
        context = {
            'respondent_count': respondent_count,
            'questions': new_questions
        }

    return context


def statistics(request):
    
    surveys_count = Survey.objects.count()
    if not surveys_count:
        return render(request, 'main/error.html', {'err_code': '404', 'error': "Надо же... ни одного опроса нет ещё..."})
    stats = []
    surveys = Survey.objects.all()
    for survey in surveys:
        try:
            survey_stats = get_results(survey.id)
        except (IndexError, TypeError):
            return render(request, 'main/error.html', {'err_code': '404', 'error': "Не удалось получить результаты опроса"})
        survey_stats['title'] = survey.text
        stats.append(survey_stats)
    context = {
        'stats': stats
    }
    return render(request, 'main/statistics.html', context=context)