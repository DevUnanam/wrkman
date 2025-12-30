from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Form for adding reviews"""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'would_recommend']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
                attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-lime-500 focus:border-transparent'
                }
            ),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-lime-500 focus:border-transparent',
                'placeholder': 'Review title (optional)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-lime-500 focus:border-transparent',
                'placeholder': 'Share your experience with this artisan...',
                'rows': 5
            }),
            'would_recommend': forms.CheckboxInput(attrs={
                'class': 'rounded text-lime-600 focus:ring-lime-500'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = 'Overall Rating'
        self.fields['title'].label = 'Review Title'
        self.fields['comment'].label = 'Your Review'
        self.fields['would_recommend'].label = 'Would you recommend this artisan?'