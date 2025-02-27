from django import forms
from .models import Review, UserProfile
from django.contrib.auth.models import User


class ReviewForm(forms.ModelForm):
    """Form for users to add a review on a trail."""
    class Meta:
        model = Review
        fields = ['pictures', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review...'}),
        }

class UserProfileForm(forms.ModelForm):
    """Form for users to update their profile."""
    class Meta:
        model = UserProfile
        fields = ['personal_image', 'favorite_trail']
        widgets = {
            'favorite_trail': forms.Select(attrs={'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)