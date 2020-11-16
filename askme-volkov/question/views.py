from django.core.paginator import Paginator
from django.shortcuts import render
from question.models import Profile, Question, Answer, Tag
from django.http import HttpResponseNotFound

questions_per_page = 3
answer_per_page = 3
top_tags_amount = 15
top_users_amount = 8
pages_around_current = 3


def paginate(objects_list, page_size, request):
    paginator = Paginator(objects_list, page_size)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return page, paginator


def get_page_range(page_range, curr_page, pages_left, pages_right=None):
    pages_right = pages_right or pages_left

    right_end = curr_page + pages_right - 1
    if right_end > len(page_range):
        right_end = len(page_range)

    left_end = curr_page - pages_left
    if left_end < 1:
        left_end = 0

    return page_range[left_end:right_end]


def index(request):
    all_questions = Question.objects.get_queryset()
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)
    page, paginator = paginate(all_questions, questions_per_page, request)
    page_range = get_page_range(page_range=paginator.page_range, curr_page=page.number,
                                pages_left=pages_around_current, pages_right=pages_around_current)

    return render(request, 'index.html',
                  {'questions': page.object_list,
                   'page': page,
                   'page_range': page_range,
                   'best_users': best_users,
                   'popular_tags': popular_tags})


def best(request):
    all_questions = Question.objects.best()
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)
    page, paginator = paginate(all_questions, questions_per_page, request)
    page_range = get_page_range(page_range=paginator.page_range, curr_page=page.number,
                                pages_left=pages_around_current, pages_right=pages_around_current)

    return render(request, 'index.html',
                  {'questions': page.object_list,
                   'page': page,
                   'page_range': page_range,
                   'best_users': best_users,
                   'popular_tags': popular_tags})


def new(request):
    all_questions = Question.objects.new()
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)
    page, paginator = paginate(all_questions, questions_per_page, request)
    page_range = get_page_range(page_range=paginator.page_range, curr_page=page.number,
                                pages_left=pages_around_current, pages_right=pages_around_current)

    return render(request, 'index.html',
                  {'questions': page.object_list,
                   'page': page,
                   'page_range': page_range,
                   'best_users': best_users,
                   'popular_tags': popular_tags})


def question(request, qid):
    curr_question = Question.objects.by_question_id(qid)
    if curr_question is None:
        return HttpResponseNotFound(f"<h1>Question {qid} does not exist!</h1>")

    answers = Answer.objects.by_question_id(qid)
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)

    page, paginator = paginate(answers, answer_per_page, request)
    page_range = get_page_range(page_range=paginator.page_range, curr_page=page.number,
                                pages_left=pages_around_current, pages_right=pages_around_current)
    return render(request, 'question.html',
                  {'question': curr_question,
                   'answers': page.object_list,
                   'page': page,
                   'page_range': page_range,
                   'best_users': best_users,
                   'popular_tags': popular_tags})


def ask(request):
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)
    return render(request, 'ask.html',
                  {'best_users': best_users,
                   'popular_tags': popular_tags})


def tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)
    page, paginator = paginate(questions, questions_per_page, request)
    page_range = get_page_range(page_range=paginator.page_range, curr_page=page.number,
                                pages_left=pages_around_current, pages_right=pages_around_current)

    return render(request, 'tag.html',
                  {'questions': page.object_list,
                   'page': page,
                   'page_range': page_range,
                   'tag_name': tag_name,
                   'best_users': best_users,
                   'popular_tags': popular_tags})


def settings(request):
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)
    return render(request, 'settings.html',
                  {'best_users': best_users,
                   'popular_tags': popular_tags})


def login(request):
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)
    return render(request, 'login.html',
                  {'best_users': best_users,
                   'popular_tags': popular_tags})


def register(request):
    popular_tags = Tag.objects.top(top_tags_amount)
    best_users = Profile.objects.top(top_users_amount)
    return render(request, 'register.html',
                  {'best_users': best_users,
                   'popular_tags': popular_tags})
