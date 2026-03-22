from django import forms

from reviews.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        error_messages = {
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

