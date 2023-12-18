from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *
from django.forms import ModelForm, TextInput, Textarea, Select, DateInput
from django import forms

class TaskForm(ModelForm):

    input_formats=['%d.%m.%Y'],

    author = forms.ModelChoiceField(queryset=User.objects.all())


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = user

    class Meta:
        model = Task
        fields = ["title", "task", "importance", "date_of_staging", "comments", "status"]
        widgets = {
            "title": TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Введите название задачи',
            }),
            "task": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите задачу',
            }),
            "importance": Select(choices=Task.IMPORTANCE, attrs={
                'class': 'form-control',
            }),
            "date_of_staging": DateInput(attrs={
                'class': 'form-control',
                'disabled': 'True',
            }),
            "comments": Textarea(attrs={
                'class': 'form-control',
                'placeholder': '',
            }),
            "status": Select(choices=Task.STATUS_CHOICES, attrs={
                'class': 'form-control',
            }),
        }

