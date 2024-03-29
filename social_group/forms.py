# forms.py
from django import forms
from .models import SocialGroup
from .models import SocialGroupPost, Comment
from .models import SocialGroupEvent


class SocialGroupForm(forms.ModelForm):
    class Meta:
        model = SocialGroup
        fields = ['name', 'description', 'privacy']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'privacy': forms.RadioSelect(),
        }


class SocialGroupPostForm(forms.ModelForm):
    class Meta:
        model = SocialGroupPost
        fields = ['content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class SocialGroupEventForm(forms.ModelForm):
    class Meta:
        model = SocialGroupEvent
        fields = ['name', 'description', 'budget', 'sponsors', 'is_tournament']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'sponsors': forms.Textarea(attrs={'class': 'form-control'}),
            'is_tournament': forms.Select(attrs={'class': 'form-control'}),
        }

