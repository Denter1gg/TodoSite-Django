from django.shortcuts import render, redirect

from .forms import TaskForm
from .models import Task, Comment

ASSETS_ROOT = "/static/assets"


def tables(request):
    tasks = Task.objects.order_by("-pk")
    comments = Comment.objects.all()

    context = {
        'ASSETS_ROOT': ASSETS_ROOT,
        'tasks': tasks,
        'comments': comments,
    }

    return render(request, 'main/tables.html', context)


def create_task(request):
    if request.method == 'POST':

        add_task_form = TaskForm(request.POST, user=request.user)

        if add_task_form.is_valid():

            task = add_task_form.save(commit=False)
            task.author = request.user

            task.save()
            print(
                f'Создана Задача с айди {task.pk}, автор задачи: {task.author}, название задачи: {task.title}, дата создания: {task.date_of_staging}.')
            return redirect('home')
        else:
            print('Форма неверная')
    else:
        add_task_form = TaskForm()

    context = {
        'ASSETS_ROOT': ASSETS_ROOT,
        'add_task_form': add_task_form,
    }

    return render(request, 'main/create-task.html', context)

def create_comment(request):
    if request.method == 'POST':

        add_comment = Comment(request.POST, user=request.user)

        if add_comment.is_valid():

            comment = add_comment.save(commit=False)
            comment.author = request.user

            comment.save()
            print(
                f'Создана Задача с айди {comment.name}, автор задачи: {comment.task}, название задачи: {comment.body}, дата создания: {comment.date_added}.')
            return redirect('home')
        else:
            print('Форма неверная')
    else:
        add_comment = TaskForm()

    context = {
        'ASSETS_ROOT': ASSETS_ROOT,
        'add_task_form': add_comment,
    }
    return render(request, 'main/create-comment.html', context)
