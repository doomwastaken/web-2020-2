from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
import random
#from app.models import Question, Author, Answer, Tag
from django.contrib import auth
#from app.forms import AskForm, AuthorForm
# Create your views here.

def index(request):
    return render(request,'index.html', {})

def notFound(request):
    return HttpResponseNotFound("hello")


def create_paginator(request, data):
    data_list = data
    paginator = Paginator(data_list, 5) # Show 5 contacts per page
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    return page


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

#@login_required
def settings(request):
    if request.POST:
        form = AuthorForm(
            data = request.POST,
            files=request.FILES,
            instance = request.user.author)
        if form.is_valid():
            form.save()
            return redirect(reverse("settings"))
    else:
        form = AuthorForm(
                    instance = request.user.author)
    return render(request, 'settings.html', {
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
    })


#@login_required
def ask(request):
    if request.POST:
        form = AskForm(request.user.author, request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse("question", kwargs={'qid' : question.pk}))
    else:
        form = AskForm(request.user.author)
    return render(request, 'ask.html', {
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
        'form' : form,
    })


def hot(request):
    page = create_paginator(request, Question.objects.hot())
    return render(request, 'hot.html', {
        'data_for_paginator': page,
        'tags' : Tag.objects.best_tags()[0:20],
        'best_members': Author.objects.best_members()[0:10],
    })



def question(request, qid):
    ## get_object_or_404
    try:
        Question.objects.get(id=qid)
    
        page = create_paginator(request, Question.objects.get(id=qid).answer_set.all())
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

def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            next_to = request.POST.get('next', '/index/')
            return redirect(next_to)
    return render(request, 'login.html', {
            'tags' : Tag.objects.best_tags()[0:20],
            'best_members': Author.objects.best_members()[0:10],
    })

def logout(request):
    auth.logout(request)
    return redirect(reverse("index"))