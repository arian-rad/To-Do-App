from django import forms
from mysite.models import Task


class DateInput(forms.DateInput):
    input_type = 'datetime-local'


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'deadline_date', 'description', 'reminder')
        labels = {
            'reminder': 'remind me'
        }

        widgets = {
            'deadline_date': DateInput(),
            'reminder': DateInput(),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5})
        }
