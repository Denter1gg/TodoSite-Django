from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.text import slugify


class Task(models.Model):

    STATUS_CHOICES = (
        ('Не начато', 'Не начато'),
        ('В работе', 'В работе'),
        ('Готово', 'Готово'),
    )

    IMPORTANCE = (
        ('Срочно', 'Срочно'),
        ('Не срочно', 'Не срочно'),
    )

    title = models.CharField('Название', max_length=50, blank=True, null=True)
    task = models.TextField('Задача', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Создатель', related_name='task_creator')
    date_of_staging = models.DateTimeField('Дата создания', default=datetime.now, null=True, blank=True)
    importance = models.CharField('Важность', max_length=50, choices=IMPORTANCE, default='Не очень')
    # comments = models.TextField('Комментарии', null=True, blank=True)
    executor = models.ForeignKey(User, verbose_name='Исполнители', on_delete=models.CASCADE, null=True, blank=True, max_length=50, related_name='task_executor')
    status = models.CharField('Статус', max_length=50, choices=STATUS_CHOICES, default='Новая Задача')
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name='URL', null=True, blank=True)
    number = models.IntegerField('Номер', default='1')

    def save(self, *args, **kwargs):
        print("Saving task...")


        slug_text = f'{self.title}-{self.id}'
        self.slug = slugify(slug_text)

        user = kwargs.pop('user', None)
        if user:
            self.author = user

        super(Task, self).save(*args, **kwargs)
        print("Task saved.")

    def __str__(self):
        return f"{self.title} {self.task} {self.date_of_staging} {self.importance}"
        # {self.comments}

    class Meta:
        verbose_name='Задача'
        verbose_name_plural='Задачи'

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField('Дата Создания', default=datetime.now, null=True, blank=True)

    def __str__(self):
        return '%s - %s' %  (self.task.title, self.name)

class Image(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images', null=True, verbose_name='задача',)
    image = models.ImageField('Изображение', null=True, upload_to='images/', blank=True)

class ChatMessage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача',)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель',)
    message = models.TextField('Сообщение', blank=True, null=True, )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано в',)

    def __str__(self):

        return f"{self.sender} {self.message}"

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'