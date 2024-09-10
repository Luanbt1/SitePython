from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Assign to')

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].empty_label = "Select user"