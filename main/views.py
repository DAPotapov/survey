from django.db import DataError, connections
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Question, Choice, Survey, UsersActivity


# Create your views here.
def index(request):
    """Стартовая страница приложения показывает перечень имеющихся опросов"""
    # В задании указано требование "Без использования ORM" только перед требованиями к
    # результатам опросов. Следовательно, в остальных местах допускается использование ORM.
    surveys = Survey.objects.all()

    # Каждый запрос на главную страницу создаёт новую сессию,
    # удобно для заполнения таблицы с результатами
    # request.session.create()
    content = {"header": "Доступные опросы", "surveys": surveys}
    return render(request, "main/index.html", content)


def treat_survey(request):
    """
    Функция обрабатывает выбор опроса пользователем
    и перенаправляет на страницу с вопросами
    """

    # Отправляем пользователя на главную страницу, 
    # если он попытался зайти по прямой ссылке
    if request.method != "POST":
        return redirect("/")

    # Если пользователь выбрал опрос

    # Заготавливаем данные для сообщения об ошибке
    err_code = "404"
    error = "Упс! Что-то пошло не так..."

    # Получаем идентификатор выбранного опроса
    survey_id = request.POST.get("survey")
    try:
        survey = Survey.objects.get(pk=survey_id)
    except (Survey.DoesNotExist, Question.MultipleObjectsReturned):
        return render(
            request, "main/error.html", {"err_code": err_code, "error": error}
        )
    else:
        # Проверка, что пользователь не проходил опрос, 
        # Если проходил, то перенаправляем на главную вместе со всплывающим сообщением
        finished_surveys = UsersActivity.objects.filter(
            question__survey_id=survey_id,
            user_id=request.session.session_key
            )
        if finished_surveys.exists():
            messages.info(request, 'Вы уже проходили этот опрос')
            return redirect('/')

        # Запоминаем выбранный опрос в сессии
        request.session["survey"] = {
            "id": survey.id,
            "text": survey.text,
            "description": survey.description,
        }

        # Задаем первый вопрос пользователю с вариантами ответа
        # или перенаправляем на страницу с ошибкой, если что-то не так
        question = survey.first_question
        choices = Choice.objects.filter(question__id=question.id)
        if choices.exists():
            header = {
                "text": survey.text,
                "description": survey.description,
            }
            context = {
                "header": header,
                "question": question,
                "choices": choices,
            }
            return render(request, "main/questions.html", context)
        else:
            return render(
                request, "main/error.html", {"err_code": err_code, "error": error}
            )




def treat_answer(request):
    """
    Функция запоминает ответы пользователя на вопрос и
    показывает следующий вопрос.
    После окончания опроса перенаправляет на страницу с результатами
    """

    if request.method == "POST":
        err_code = "404"
        error = "Упс! Что-то пошло не так..."

        survey = request.session.get("survey", "")

        # Получаем информацию о вопросе и ответе на него из формы
        try:
            question_id, choosen_id = request.POST.get("choice").split("_")
        except AttributeError:
            return render(
                request, "main/error.html", {"err_code": err_code, "error": error}
            )

        # Записываем полученную информацию в БД
        try:
            question = Question.objects.get(pk=question_id)
            choice = Choice.objects.get(pk=choosen_id)
            answer = UsersActivity(
                user_id=request.session.session_key, question=question, choice=choice
            )
            answer.save()
        except (
            Question.DoesNotExist,
            Question.MultipleObjectsReturned,
            Choice.DoesNotExist,
            Choice.MultipleObjectsReturned,
        ):
            return render(
                request, "main/error.html", {"err_code": err_code, "error": error}
            )
        except DataError:
            err_code = "500"
            error = "Не удалось записать в базу данных. Попробуйте позже."
            return render(
                request, "main/error.html", {"err_code": err_code, "error": error}
            )
        else:
            # Если ответ никуда не ведёт, значит опрос закончен и пора показывать результаты
            if not choice.next_question:
                stats = []
                try:
                    survey_results = get_results_raw_sql(
                        request.session.get("survey", "")["id"]
                    )
                    survey_results["title"] = survey["text"]
                except (AttributeError, ValueError, IndexError, TypeError):
                    return render(
                        request,
                        "main/error.html",
                        {"err_code": err_code, "error": error},
                    )
                else:
                    stats.append(survey_results)
                    context = {"stats": stats}
                    return render(request, "main/statistics.html", context=context)

            # Готовим следующий вопрос и варианты ответа на него
            try:
                question = choice.next_question
            except (Question.DoesNotExist, Question.MultipleObjectsReturned):
                return render(
                    request, "main/error.html", {"err_code": err_code, "error": error}
                )
            else:
                choices = question.choices.all()
                if choices.exists():
                    context = {
                        "header": survey,
                        "question": question,
                        "choices": choices,
                    }
                    return render(request, "main/questions.html", context)
                else:
                    return render(
                        request,
                        "main/error.html",
                        {"err_code": err_code, "error": error},
                    )

    else:
        return redirect("/")


def get_results_raw_sql(survey_id):
    """
    Функция подготавливает результаты опроса по заданному id.
    С использованием raw-SQL-запросов.
    """

    # Подключаемся к БД
    db_name = "default"
    conn = connections[db_name]
    survey_stats = {}
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

        # Объединим полученные данные, преобразовав в словарь
        c_keys = ["text", "question_id", "choice_count"]
        new_questions = []
        q_keys = ["id", "text", "record_count", "position"]
        for q in questions:
            question = dict(zip(q_keys, q))
            q_choices = []
            for c in choices:
                choice_dict = dict(zip(c_keys, c))
                if choice_dict["question_id"] == question["id"]:
                    choice_dict["rate"] = (
                        choice_dict["choice_count"] / question["record_count"] * 100
                    )  # процент
                    q_choices.append(choice_dict)
            question["choices"] = q_choices
            question["rate"] = (
                question["record_count"] / respondent_count * 100
            )  # процент
            new_questions.append(question)

        # Соберём словарь для передачи в вызывающую функции, а затем в шаблон
        survey_stats = {
            "respondent_count": respondent_count,
            "questions": new_questions,
        }

    return survey_stats


def get_results_orm(survey_id):
    """
    Функция подготавливает результаты опроса по заданному id.
    С использованием ORM.
    """
    
    # Всего респондентов
    respondent_count = UsersActivity.objects.filter(
        question__survey_id=survey_id).distinct().count()



    return respondent_count

def statistics(request):
    """
    Функция заполняет страницу со статистикой.
    """

    surveys_count = Survey.objects.count()
    if not surveys_count:
        return render(
            request,
            "main/error.html",
            {"err_code": "404", "error": "Надо же... ни одного опроса нет ещё..."},
        )
    stats = []
    surveys = Survey.objects.all()

    # Для каждого запроса в БД получаем результаты из соответствующей функции
    for survey in surveys:
        try:
            survey_stats = get_results_raw_sql(survey.id)
        except (IndexError, TypeError):
            return render(
                request,
                "main/error.html",
                {"err_code": "404", "error": "Не удалось получить результаты опроса"},
            )
        survey_stats["title"] = survey.text
        stats.append(survey_stats)
    context = {"stats": stats}
    return render(request, "main/statistics.html", context=context)
