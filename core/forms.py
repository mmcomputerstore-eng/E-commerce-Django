from django import forms
from core.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write review',
            'rows': 4,
            'id': 'review'
        })
    )

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control',
                'id': 'rating'
            })
        }