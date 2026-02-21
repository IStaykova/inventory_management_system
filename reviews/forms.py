from django import forms

from reviews.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        error_messages = {
            'author_name': {
                'required': 'Name is required',
                'min_length': 'Name must be at least 2 characters long.',
            },
            'rating': {
                'required': 'Rating is required',
                'min_value': 'Rating must be between 1 and 5.',
                'max_value': 'Rating must be between 1 and 5.',
            },
            'text': {
                'required': 'Text is required',
                'min_length': 'Review must be at least 10 characters long.'
            }
        }

