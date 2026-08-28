from typing import ClassVar

from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields: ClassVar[list[str]] = ['title', 'description', 'completed']
