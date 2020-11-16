from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
import random
from app.models import Question, Author, Answer, Tag

# Create your views here.

def notFound(request):
    return HttpResponseNotFound("hello")


def create_paginator(request, data):
    data_list = data
    paginator = Paginator(data_list, 5) # Show 5 contacts per page
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return page

def login(request):
    return render(request, 'login.html', {
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
    })


def index(request):
    page = create_paginator(request, Question.objects.newest())
    return render(request, 'index.html', {
        'data_for_paginator': page,
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
    }) #{} - словарик для параметров (переменных)

def register(request):
    return render(request, 'register.html', {
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
    })

def settings(request):
    return render(request, 'settings.html', {
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
    })


def ask(request):
    return render(request, 'ask.html', {
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
    })


def hot(request):
    page = create_paginator(request, Question.objects.hot())
    return render(request, 'hot.html', {
        'data_for_paginator': page,
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
    })



def question(request, qid):
    try:
        Question.objects.get(id=qid)
        page = create_paginator(request, Question.objects.get(id=qid).answers.all())
        return render(request, 'question.html', {
            'question': Question.objects.get(id=qid),
            'qid': qid,
            'data_for_paginator' : page,
            'tags' : Tag.objects.best_tags()[0:20],
            'best_members': Author.objects.best_members()[0:10],
        })
    except Question.DoesNotExist:
        return render(request, '404.html')


def tag(request, tag_name):
    try:
        t = Tag.objects.get(title=tag_name)
        page = create_paginator(request, Question.objects.filter(tags__title = tag_name))
        return render(request, 'tagsort.html', {
            'data_for_paginator': page,
            'tags' : Tag.objects.best_tags()[0:20],
            'best_members': Author.objects.best_members()[0:10],
            'tag': t,
            'tag_name': tag_name,
        })
    except Tag.DoesNotExist:
         return render(request, '404.html')
