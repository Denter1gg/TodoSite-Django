from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *
from django.forms import ModelForm, TextInput, Textarea, Select, DateInput
from django import forms

class TaskForm(ModelForm):

    input_formats=['%d.%m.%Y'],

    author = forms.ModelChoiceField(queryset=User.objects.all(), initial=User.objects.first(), required=False,
                                    widget=forms.Select(attrs={'style': 'display:none;', }))


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = user

    class Meta:
        model = Task
        fields = ["title", "task", "importance", "author", "date_of_staging", "status"] # "comments",
        widgets = {
            "title": TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Введите название задачи',
            }),
            "task": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите свою задачу',
            }),
            "importance": Select(choices=Task.IMPORTANCE, attrs={
                'class': 'form-control',
            }),
            "date_of_staging": DateInput(attrs={
                'class': 'form-control',
                'disabled': 'True',
            }),
            # "comments": Textarea(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Комментарии',
            # }),
            "status": Select(choices=Task.STATUS_CHOICES, attrs={
                'class': 'form-control',
            }),
        }

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ["task", "name", "body", "date_added"]
        widgets = {
            "task": TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Введите название задачи',
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задачи',
            }),
            "body": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название задачи',
            }),
            "date_added": DateInput(attrs={
                'class': 'form-control',
                # 'disabled': 'True',
            }),
        }

