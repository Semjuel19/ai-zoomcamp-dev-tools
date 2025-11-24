from django import forms
from .models import TODO


class TODOForm(forms.ModelForm):
    """Form for creating and editing TODOs"""
    
    class Meta:
        model = TODO
        fields = ['title', 'description', 'due_date', 'is_resolved']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter TODO title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_resolved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'due_date': 'Due Date',
            'is_resolved': 'Mark as Resolved',
        }
