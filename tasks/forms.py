from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form class for users to create a task
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'estimated_minutes', 'due_date', 'completed']

    def clean_estimated_minutes(self):
        value = self.cleaned_data.get('estimated_minutes')
        # Allow empty (none) but if provided must be > 0
        if value is not None and value <= 0:
            raise forms.ValidationError("Estimated minutes must be greater than 0.")
        return value
