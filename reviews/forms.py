from django import forms

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1,
                                max_value=5,
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}))

    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_rating(self):
        r = self.cleaned_data['rating']
        if r < 1 or r > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return r

    def clean_text(self):
        t = (self.cleaned_data['text'] or '').strip()
        if len(t) < 10:
            raise forms.ValidationError('Review must be at least 10 characters long.')
        return t

