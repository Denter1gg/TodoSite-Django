from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Создатель')
    date_of_staging = models.DateTimeField('Дата создания', default=datetime.now, null=True, blank=True)
    importance = models.CharField('Важность', max_length=50, choices=IMPORTANCE, default='Не очень')
    # comments = models.TextField('Комментарии', null=True, blank=True)
    # executor = models.CharField('Исполнители', max_length=50, )
    status = models.CharField('Статус', max_length=50, choices=STATUS_CHOICES, default='Новая Задача')


    def save(self, *args, **kwargs):
        print("Saving task...")


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
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' %  (self.task.title, self.name)