from django import forms


class StudentForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    hackerrank_username = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'your_hackerrank_username (optional)'
        })
    )
    cgpa = forms.FloatField(
        min_value=0.0, max_value=10.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.0 – 10.0',
            'step': '0.01'
        })
    )
    internships = forms.IntegerField(
        min_value=0, max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of internships'
        })
    )
    projects = forms.IntegerField(
        min_value=0, max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of projects'
        })
    )
    technical_skills_score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Score out of 100'
        })
    )
    hackerrank_score = forms.IntegerField(
        min_value=0, max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Score out of 100'
        })
    )