import uuid

from PIL import Image as PILImage
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.template.loader import render_to_string
from requests import post

from .forms import *
from .models import *

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

            image_files = request.FILES.getlist('image')
            # except Exception as e:
            #     print(e)
            for image_file in image_files:
                print(image_file)
                PILImage.open(image_file)
                fs = FileSystemStorage()
                unique_filename = f"{uuid.uuid4()}_{slugify(image_file.name)}"
                # сохранение файлa на сервере
                filename = fs.save(unique_filename, image_file)

                image_path = fs.url(filename)

                # создание файла
                image = Image.objects.create(
                    task=task,
                    image=image_path,
                )

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

        add_comment = CommentForm(request.POST, user=request.user)

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
        add_comment = CommentForm()

    context = {
        'ASSETS_ROOT': ASSETS_ROOT,
        'add_comment': add_comment,
    }
    return render(request, 'main/create-comment.html', context)


def edit_task_view(request, task_slug):
    task_for_edit = get_object_or_404(Task, slug=task_slug)

    if request.POST:
        form = EditTaskForm(request.POST, instance=task_for_edit)
        if form.is_valid():
            pass
        else:
            print(form.errors)
    else:
        form = EditTaskForm(instance=task_for_edit)

    context = {
        'task_for_edit': task_for_edit,
        'ASSETS_ROOT': ASSETS_ROOT,
        'form': form,
    }

    return render(request, 'main/edit_task.html', context)


def add_messages_view(request):
    if request.method == "POST":
        task_id = request.POST.get('task_id')
        task_for_edit_messages = get_object_or_404(Task, pk=task_id)

        send_message = ChatMessage.objects.create(
            task=task_for_edit_messages,
            sender=request.user,
            message=request.POST.get('message'),
        )

        image_files = request.FILES.getlist('image')
        # except Exception as e:
        #     print(e)
        for image_file in image_files:
            print(image_file)
            PILImage.open(image_file)
            fs = FileSystemStorage()
            unique_filename = f"{uuid.uuid4()}_{slugify(image_file.name)}"
            # сохранение файлa на сервере
            filename = fs.save(unique_filename, image_file)

            image_path = fs.url(filename)

            # создание файла
            image = Image.objects.create(
                post=post,
                image=image_path,
            )

        print("send_message: ", send_message)

        send_message.save()


        messages = ChatMessage.objects.filter(task = task_for_edit_messages).order_by('created_at')
        message_sender = send_message.sender
        sender_name = message_sender.first_name
        print('sender_name: ', sender_name)
        messages_with_senders = [{'message': message, 'sender_name': message.sender.first_name} for message in messages]

        html = render_to_string('main/messages.html', {'messages_with_senders': messages_with_senders})
        return JsonResponse({'success': True, 'html': html})
    else:
        return JsonResponse({'success': False})