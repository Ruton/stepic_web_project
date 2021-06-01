# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404, redirect
from qa.models import Question, Answer
from qa.forms import AnswerForm, AskForm

def test(request, *args, **kwargs):
    return HttpResponse('OK')

@require_GET
def home(request):
    questions = Question.objects.new()
    paginator, page = paginate(request, questions)

    return render(request, 'qa/home.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


@require_GET
def popular(request):
    questions = Question.objects.popular()
    paginator, page = paginate(request, questions)

    return render(request, 'qa/popular.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
    })


def question(request, id):
    if request.method == "POST":
        return HttpResponse('OK')
    question = get_object_or_404(Question, pk=id)
    answers = Answer.objects.filter(question=id)
    answer_form = AnswerForm({'question': question.id})

    return render(request, 'qa/question.html', {
        'question': question,
        'answers': answers,
        'form': answer_form,
    })


@require_POST
def answer(request):
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save()
        return HttpResponseRedirect(question.id)


def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'qa/ask.html', {'form': form})


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10

    if limit > 100:
        limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return paginator, page
