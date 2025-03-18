from django import forms
from .models import Review, UserProfile, Trail
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class ReviewForm(forms.ModelForm):
    """Form for users to add a review on a trail."""
    class Meta:
        model = Review
        fields = ['pictures', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review...'}),
        }

class UserProfileForm(forms.ModelForm):
    """Form for users to update their profile information."""
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    personal_bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)

    class Meta:
        model = UserProfile
        fields = ['personal_image', 'personal_bio']


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom Password Change Form with Bootstrap styling."""
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class FavoriteTrailForm(forms.ModelForm):
    favorite_trails = forms.ModelMultipleChoiceField(
        queryset=Trail.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['favorite_trails']


class TrailForm(forms.ModelForm):
    LEVEL_CHOICES = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Hard', 'Hard'),
    ]

    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    length = forms.FloatField(
        label="Length (km)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 5.4'
            }
        )
    )

    estimate_time = forms.FloatField(
        label="Estimate Time (hours)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2.5'
            }
        )
    )

    class Meta:
        model = Trail
        fields = [
            'title',
            'length',
            'estimate_time',
            'level',
            'elevation_gain',
            'latitude',
            'longitude'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'elevation_gain': forms.NumberInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }